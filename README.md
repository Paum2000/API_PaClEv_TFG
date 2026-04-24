# API PaClEv 

API robusta y asíncrona desarrollada para el Trabajo de Fin de Grado **PaClEv**. Construida con **FastAPI**, arquitectura de base de datos **NoSQL (MongoDB)** y totalmente contenedorizada con **Docker** para un despliegue ágil y reproducible.

> ** Nota sobre las ramas del repositorio:** Este repositorio cuenta con dos ramas principales — `sql` y `mongo` — resultado de un estudio comparativo de rendimiento realizado con **Locust**. Tras las pruebas, **MongoDB fue seleccionado** como base de datos definitiva. Los resultados del benchmark están documentados [más abajo](#-benchmark-de-rendimiento-sql-vs-mongodb).

---

## Funcionalidades Principales

| Módulo | Descripción |
|---|---|
| **Usuarios** | Registro, login y subida de fotos de perfil |
| **Autenticación** | Login con tokens JWT y contraseñas encriptadas con Bcrypt |
| **Eventos** | CRUD completo de eventos en el calendario |
| **Tareas** | Gestión de tareas con seguimiento de estado (completado/pendiente) |
| **Temas** | Gestión de temas visuales para la interfaz *(solo administradores)* |
| **Ajustes** | Personalización de idioma, colores y tema por usuario |

---

## Stack Tecnológico

- **Framework backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **Base de datos:** [MongoDB](https://www.mongodb.com/) con motor asíncrono
- **ODM:** [Beanie](https://beanie-odm.dev/) (Object Document Mapper basado en Pydantic)
- **Seguridad:** OAuth2 (JWT) + Passlib (Bcrypt)
- **Despliegue:** Docker & Docker Compose
- **Testing:** Pytest, HTTPX y Pytest-Asyncio

---

## Arquitectura del Sistema

El proyecto sigue el patrón de **Clean Architecture** para garantizar la separación de responsabilidades y la escalabilidad del código:

```
app/
├── models/      # Definición de documentos MongoDB mediante Beanie
├── schemas/     # Modelos de validación de datos (entrada/salida) con Pydantic
├── routers/     # Endpoints y gestión de rutas HTTP
├── services/    # Lógica de negocio (intermediaria entre routers y base de datos)
└── core/        # Configuraciones centrales, seguridad y variables de entorno
tests/           # Batería de pruebas automatizadas
```

---

## Puesta en Marcha

### 1. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente configuración:

```env
# Conexión a Base de Datos
MONGO_URL=mongodb://mongodb:27017
DB_NAME=agenda_db

# Seguridad JWT
SECRET_KEY=3ae6742be2863eaff31865e1f3f8132305f011b25d14de395f63401254d153b8
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Acceso Documentación y Admin inicial
SWAGGER_USER=admin
SWAGGER_PASSWORD=admin1234
FIRST_ADMIN_EMAIL=admin@miproyecto.com
FIRST_ADMIN_PASSWORD=admin1234
```

### 2. Despliegue con Docker

Levanta la infraestructura completa (API + MongoDB) en un solo paso:

```bash
docker-compose up --build
```

La API estará disponible en: **http://localhost:8000**

---

## Endpoints Principales

Todos los endpoints privados requieren el token JWT en la cabecera `Authorization: Bearer <token>`.

### Autenticación
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/auth/login` | Inicio de sesión y generación de JWT |

### Usuarios
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/users/` | Registro de nuevo usuario |
| `GET` | `/users/me` | Obtener datos del usuario actual |
| `PUT` | `/users/me` | Actualizar perfil |

### Eventos y Tareas
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/events/me` | Lista de eventos del usuario |
| `GET` | `/tasks/me` | Lista de tareas del usuario |

### Ajustes
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/settings/me` | Obtener configuración personalizada |

---

## Documentación Interactiva 

La API incluye documentación autogenerada con **Swagger UI**, protegida por Basic Auth para prevenir accesos no autorizados.

- **URL:** http://localhost:8000/docs
- **Credenciales:** definidas en `SWAGGER_USER` y `SWAGGER_PASSWORD` del archivo `.env`

---

## Benchmark de Rendimiento: SQL vs MongoDB

Para determinar la base de datos más adecuada para el proyecto, se llevaron a cabo pruebas de carga y rendimiento con **[Locust](https://locust.io/)**, simulando tráfico real de usuarios concurrentes sobre ambas implementaciones.

### Resultados

| Métrica | SQL (PostgreSQL) | MongoDB | Ganador |
|---|------------------|---|---|
| **Velocidad de respuesta** | Línea base       | ~3× más rápido | MongoDB |
| **Tasa de fallos** | 7%               | 1% | MongoDB |

### Conclusiones

MongoDB demostró una ventaja clara en ambas métricas críticas: triplicó la velocidad de respuesta bajo carga y redujo la tasa de errores del 7% al 1%. Estos resultados justifican la elección de MongoDB como base de datos definitiva del proyecto.

La implementación SQL se conserva en la rama `sql` del repositorio para consulta y comparación.

---

## Testing y Calidad del Código

Se ha implementado una estrategia de pruebas exhaustiva con **pytest**, superando una batería de **23 tests automatizados** que validan:

- Flujo completo de registro y autenticación (Happy Path & Sad Path)
- Operaciones CRUD seguras en Tareas y Eventos
- Protección contra accesos no autorizados (Error 401 y 403)
- Validación estricta de esquemas Pydantic (Error 422)

### Ejecutar los tests

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

Al finalizar, se genera automáticamente un **reporte de cobertura** en formato HTML navegable disponible en `htmlcov/index.html`.

---

*Desarrollado por Paula — Proyecto TFG 2026*
