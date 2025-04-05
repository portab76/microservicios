 # Auth-Service

Microservicio de autenticaci��n JWT para sistemas distribuidos

## Descripci��n

Servicio Spring Boot que provee:
- Autenticaci��n basada en JWT
- Validaci��n de tokens
- Integraci��n con bases de datos MySQL
- Configuraci��n para entornos Docker/Kubernetes

## Requisitos

- Java 17+
- MySQL 8.0+
- Maven 3.8+
- Docker (opcional)

## API Endpoints

Pruebas B��sicas con Postman

### Autentica un usuario y genera token JWT

```
POST http://localhost:8080/auth/login
Content-Type: application/json
{
  "username": "admin",
  "password": "admin123"
}
```
Response:
200 OK (usuario v��lido)
```
json
{
  "token": "string",
  "id": long,
  "username": "string",
  "email": "string"
}
```
400 Bad Request (usuario contrase?a inv��lido)

curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
  
### Valida un token JWT

Se pasa el token JWT como par��metro "Authorization" en el encabezado de la solicitud (header).

http://localhost:8080/auth/validate

Responses:

200 OK (token v��lido)

400 Bad Request (token inv��lido)

curl -X GET http://localhost:8080/auth/validate \
  -H "Authorization: Bearer [token]"

## Docker

**Compilar Proyecto
mvn clean package

**Construir contenedor:
docker build -t auth-service .

**Ejecutar contenedor:
docker run -d -p 8080:8080 --name auth-service -e SPRING_DATASOURCE_URL=jdbc:mysql://host.docker.internal:3306/camerasdb -e SPRING_DATASOURCE_USERNAME=root -e SPRING_DATASOURCE_PASSWORD=root123 auth-service

