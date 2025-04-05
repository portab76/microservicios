
### Docker zookeeper y kafka:

**Arrancar contenedor docker-compose.yml**
docker-compose up -d

**Para contenedor**
docker-compose down -v

**Ver todos los contenedores:**
docker ps -a

**Ver log de consola contenedor**
docker logs zookeeper
docker logs kafka

** Eliminar completamente un contenedor 
docker ps -a
docker volume ls
docker stop [nombre-contenedor]
docker rm [nombre-contenedor]
docker volume rm [nombre-volumen]

### Prueba Básica (Producir/Consumir Mensajes):
 
**Entrar al contenedor de Kafka**
docker exec -it kafka bash
docker exec -it database-service-mysql_db-1 bash

**Lista todos los topics en el cluster de Kafka:**
kafka-topics --list --bootstrap-server kafka:9092 

**Crear un tema de prueba**
kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic camera-status-updates
  
**Verificar que el tema se creó**
kafka-topics --list --bootstrap-server kafka:9092

**Producir mensajes (desde dentro del contenedor)**
kafka-console-producer \
  --broker-list kafka:9092 \
  --topic camera-status-updates
Escribe algunos mensajes (ej: Hola Kafka!) y presiona Ctrl+C para salir.

**Consumir mensajes (desde dentro del contenedor)**
kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic camera-status-updates \
  --from-beginning
  