 # Auth-Service

Microservicio de autenticación JWT para sistemas distribuidos

## 📝 Descripción

Servicio Spring Boot que provee:
- Autenticación basada en JWT
- Validación de tokens
- Integración con bases de datos MySQL
- Configuración para entornos Docker/Kubernetes

## 🚀 Requisitos

- Java 17+
- MySQL 8.0+
- Maven 3.8+
- Docker (opcional)

## 📚 API Endpoints

Pruebas Básicas con Postman

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
200 OK (token válido)
```
json
{
  "token": "string",
  "id": long,
  "username": "string",
  "email": "string"
}
```
400 Bad Request (usuario contraseña inválido)

curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
  
### Valida un token JWT

Se pasa el token JWT como parámetro "Authorization" en el encabezado de la solicitud (header).

http://localhost:8080/auth/validate

Responses:

200 OK (token válido)

400 Bad Request (token inválido)

curl -X GET http://localhost:8080/auth/validate \
  -H "Authorization: Bearer [token]"

##🐳 Docker

**Construir imagen:
docker build -t auth-service .

**Ejecutar contenedor:
docker run -p 8080:8080 \
  -e SPRING_DATASOURCE_URL=jdbc:mysql://host.docker.internal:3306/authdb \
  -e SPRING_DATASOURCE_USERNAME=admin \
  -e SPRING_DATASOURCE_PASSWORD=secret \
  auth-service
🧪 Testing


##📦 Estructura del Proyecto
```
src/
├── main/
│   ├── java/
│   │   └── com/proyectocamaras/auth/
│   │       ├── config/       # Configuraciones Spring
│   │       ├── controller/   # Controladores REST
│   │       ├── model/        # Entidades JPA
│   │       ├── repository/   # Repositorios Spring Data
│   │       ├── security/     # Configuración de seguridad
│   │       └── service/      # Lógica de negocio
│   └── resources/            # Properties y configs
└── test/                     # Pruebas unitarias
```