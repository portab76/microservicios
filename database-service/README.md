# CamerasDB MySQL Service

Este proyecto utiliza Docker para levantar un contenedor con una base de datos MySQL 8.0 ya configurada. Esta pensado como entorno de desarrollo para una base de datos llamada `camerasdb`.

---

## Servicios

El archivo `docker-compose.yml` define un unico servicio:

- **mysql-server**: una instancia de MySQL 8.0 con los siguientes valores por defecto:
  - **Usuario root**: `root`
  - **Contrasena root**: `root123`
  - **Base de datos inicial**: `camerasdb`
  - **Usuario adicional**: `user`
  - **Contrasena usuario**: `user123`

---

## Como usar

1. Asegurate de tener Docker instalado.
2. En la terminal, en la misma carpeta del `docker-compose.yml`, ejecuta:

   ```
   docker-compose up -d
   ```