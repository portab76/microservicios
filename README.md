

## Sistema de monitoreo de cámaras usando una arquitectura de microservicios

Microservicios Necesarios:
- Servicio de Autenticación (Java Spring Boot)
- Servicio de Gestión de Usuarios (Java Spring Boot)
- Servicio de Cámaras (Python)
- Driver SPcam32 (Python)
- Servicio de Notificaciones (PHP)
- Servicio de Almacenamiento (Python)
- API Gateway (Node.js)
- Frontend (React/Vue)



```
[Frontend] ←→ [API Gateway] ←→ [Autenticación] ←→ [Gestión de Usuarios]
                      ↑
                      ↓
[Servicio de Cámaras] ←→ [Kafka] ←→ [Servicio de Notificaciones]
      ↑                     ↓
      |               [Servicio de Almacenamiento]
      ↓                     |
[Driver SPcam32]        [Base de Datos]
```

Primero arrancar el servicio de base de datos.