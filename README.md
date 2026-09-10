# MS1 - Clientes y Pedidos

Microservicio de gestión de clientes y pedidos para el proyecto de Cloud Computing (CS2032).

##  Tecnologías

- **Lenguaje:** Python 3.11+
- **Framework:** FastAPI
- **Base de datos:** MySQL 8.0
- **Contenedores:** Docker + Docker Compose

##  Endpoints

Documentación interactiva (Swagger UI): `http://localhost:8000/docs`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Info del servicio |
| GET | `/health` | Health check |
| GET | `/clientes` | Lista clientes |
| GET | `/clientes/{id}` | Cliente por ID |
| GET | `/clientes/{id}/pedidos` | Pedidos de un cliente |
| GET | `/clientes/buscar/?email=` | Buscar por email |
| GET | `/pedidos` | Lista pedidos (con JOIN) |
| GET | `/pedidos/{id}` | Pedido por ID |
| GET | `/pedidos/estado/{estado}` | Pedidos por estado |
| GET | `/pedidos/estadisticas/por-estado` | Estadísticas por estado |
| GET | `/clientes/estadisticas/top` | Top clientes |

##  Cómo ejecutar

### Requisitos
- Docker Desktop
- Docker Compose

### Levantar el proyecto

```bash
docker compose up -d --build
