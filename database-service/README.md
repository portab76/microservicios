# CamerasDB MySQL Service

   El archivo `docker-compose.yml` define un único servicio una instancia de MySQL 8.0.

## Cómo levantar el contenedor

1. Asegúrate de tener Docker instalado.
2. En la terminal, en la misma carpeta del `docker-compose.yml`, ejecuta:

   ```
   docker-compose up -d
   ```

3. Restaurar la base de datos 
   Debes restaurar manualmente el contenido del archivo data.sql para cargar la estructura y los datos iniciales en la base de datos camerasdb.
   Los valores de la nueva conexión a MySQL con los siguientes datos:
   ```
   Host: localhost
   Puerto: 3306
   Usuario: root
   Contraseña: root123
   ```

   **Volumen persistente**
   La base de datos se almacena en un volumen Docker llamado mysql_data, por lo que los datos no se pierden al reiniciar el contenedor.

   **Cómo detener y eliminar el contenedor**
   ```
   docker-compose down
   ```
   **Si también deseas borrar todos los datos:**
   ```
   docker-compose down -v
   ```