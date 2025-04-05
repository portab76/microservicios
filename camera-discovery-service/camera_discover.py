import json
import logging
import time
from datetime import datetime
from typing import Dict, Optional, List
import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError, NoBrokersAvailable
import mysql.connector
from mysql.connector import Error as MySQLError
import socket
import sys
import os

# Configuración avanzada de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./log/camera_discovery.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CameraDiscoveryService')

class ConfigError(Exception):
    """Excepción personalizada para errores de configuración"""
    pass

class CameraDiscoveryService:
    def __init__(self, config: Dict):
        """
        Inicializa el servicio con validación de configuración.
        Args:
            config (Dict): Configuración del servicio
        Raises:
            ConfigError: Si la configuración es inválida
        """
        try:
            self._validate_config(config)
            self.db_config = config['db_config']
            self.kafka_config = config['kafka_config']
            self.scan_interval = config.get('scan_interval', 60)
            self.camera_timeout = config.get('camera_timeout', 5)
            
            # Estado actual de las cámaras (cache local)
            self.camera_states = {}
            
            # Inicializar componentes con manejo de errores
            self._init_kafka_producer()
            self._test_db_connection()
            
        except Exception as e:
            logger.critical(f"Error inicializando el servicio: {str(e)}")
            raise ConfigError(f"Configuración inválida: {str(e)}")

    def _validate_config(self, config: Dict):
        """Valida la estructura básica de la configuración"""
        required_keys = {
            'db_config': ['host', 'user', 'password', 'database'],
            'kafka_config': ['bootstrap_servers', 'topic']
        }
        
        for section, keys in required_keys.items():
            if section not in config:
                raise ConfigError(f"Falta sección '{section}' en configuración")
            for key in keys:
                if key not in config[section]:
                    raise ConfigError(f"Falta clave '{key}' en {section}")

    def _init_kafka_producer(self):
        """Intenta inicializar el productor Kafka con manejo de errores"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self._check_kafka_connection()
                
                self.kafka_producer = KafkaProducer(
                    bootstrap_servers=self.kafka_config['bootstrap_servers'],
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    retries=max_retries,
                    request_timeout_ms=30000
                )
                logger.info("Productor Kafka inicializado correctamente")
                return
                
            except NoBrokersAvailable as e:
                logger.warning(f"Intento {attempt + 1}/{max_retries}: Kafka no disponible")
                if attempt == max_retries - 1:
                    logger.error("No se pudo conectar a Kafka después de varios intentos")
                    raise
                time.sleep(retry_delay)
                
            except KafkaError as e:
                logger.error(f"Error de Kafka: {str(e)}")
                raise ConfigError(f"Error configurando Kafka: {str(e)}")

    def _check_kafka_connection(self):
        """Verifica conectividad básica con Kafka"""
        try:
            # Verificación de puerto abierto
            host, port = self.kafka_config['bootstrap_servers'].split(':')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            
            if result != 0:
                raise ConfigError(f"No se puede conectar a Kafka en {host}:{port}")
                
        except ValueError as e:
            raise ConfigError(f"Formato inválido para bootstrap_servers: {str(e)}")

    def _test_db_connection(self):
        """Verifica que la conexión a la base de datos funciona"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            conn.close()
            logger.info("Conexión a MySQL verificada correctamente")
        except MySQLError as e:
            raise ConfigError(f"No se puede conectar a MySQL: {str(e)}")

    def fetch_cameras_from_db(self) -> Optional[List[Dict]]:
        """
        Obtiene la lista de cámaras desde la base de datos MySQL con manejo de errores.
        
        Returns:
            List[Dict] | None: Lista de cámaras o None si hay error
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, camera_name, stream_url, image_url, ip_address, description 
                FROM cameras
                WHERE is_active = 1
            """
            cursor.execute(query)
            cameras = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            logger.debug(f"Obtenidas {len(cameras)} cámaras desde la base de datos")
            return cameras
            
        except MySQLError as e:
            logger.error(f"Error de base de datos: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al obtener cámaras: {str(e)}")
            return None

    def run(self):
        """Ejecuta el servicio de descubrimiento de cámaras."""
        while True:
            cameras = self.fetch_cameras_from_db()
            if cameras:
                for camera in cameras:
                    status = self.check_camera_status(camera)
                    self.publish_status_change(camera, status)
            time.sleep(self.scan_interval)

    def check_camera_status(self, camera):
        #implementación de la lógica para chequear el estado de la camara.
        try:
            url = f"http://{camera['ip_address']}"
            response = requests.get(url, timeout = self.camera_timeout)
            if response.status_code == 200:
                return "online"
            else:
                return "offline"
        except requests.exceptions.RequestException:
            return "offline"

    def publish_status_change(self, camera, status):
        #implementacion de la lógica para publicar el cambio de estado.
        message = {
            "camera_id": camera["id"],
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        try:
            self.kafka_producer.send(self.kafka_config["topic"], message)
            logger.info(f"Estado de la cámara {camera['id']} publicado: {status}")
        except KafkaError as e:
            logger.error(f"Error al publicar mensaje en Kafka: {str(e)}")

def load_config(config_path: str) -> Dict:
    """
    Carga la configuración desde un archivo JSON con validación.
    
    Args:
        config_path (str): Ruta al archivo de configuración
        
    Returns:
        Dict: Configuración cargada
        
    Raises:
        ConfigError: Si hay problemas cargando el archivo
    """
    try:
        if not os.path.exists(config_path):
            raise ConfigError(f"Archivo de configuración no encontrado: {config_path}")
            
        with open(config_path) as f:
            config = json.load(f)
            
        # Validación básica
        if not isinstance(config, dict):
            raise ConfigError("El archivo de configuración debe ser un objeto JSON")
            
        return config
        
    except json.JSONDecodeError as e:
        raise ConfigError(f"Error parseando JSON: {str(e)}")
    except Exception as e:
        raise ConfigError(f"Error cargando configuración: {str(e)}")

def main():
    try:
        # Cargar configuración
        config = load_config('config.json')
        
        # Inicializar servicio
        service = CameraDiscoveryService(config)
        
        logger.info("Servicio iniciado correctamente")
        service.run()
        
    except ConfigError as e:
        logger.critical(f"Error de configuración: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Servicio detenido manualmente")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Error inesperado: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()