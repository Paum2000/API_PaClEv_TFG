# PaClEvAPI

> API robusta y asíncrona desarrollada para el Trabajo de Fin de Grado **PaClEv**.  
> Construida con FastAPI, arquitectura NoSQL (MongoDB) y contenedorizada con Docker para un despliegue ágil y reproducible.

---

> **Nota sobre las ramas del repositorio:** Este repositorio cuenta con dos ramas principales — `sql` y `mongo` — resultado de un estudio comparativo de rendimiento realizado con Locust. Tras las pruebas, MongoDB fue seleccionado como base de datos definitiva. Los resultados del benchmark están documentados más abajo.

---

## Funcionalidades Principales

| Módulo | Descripción |
|---|---|
| **Usuarios** | Registro, login y gestión de perfil seguro. |
| **Autenticación** | Login stateless con tokens JWT y contraseñas encriptadas (Bcrypt). |
| **Horarios** | Gestión de múltiples horarios semanales (ej. Verano/Invierno) con bloques de actividades personalizados por día y hora. |
| **Eventos** | CRUD de eventos con soporte avanzado para recurrencia y control independiente de fechas y horas. |
| **Tareas** | Gestión de tareas con seguimiento de estado, niveles de prioridad y personalización de colores. |
| **Listas** | Creación y gestión de listas personalizadas de ítems aisladas por usuario. |
| **Temas** | Gestión de temas visuales para la interfaz (solo administradores). |
| **Ajustes** | Personalización de idioma, colores de acento y temas por usuario. |

---

## Stack Tecnológico

| Categoría | Tecnología |
|---|---|
| **Framework backend** | FastAPI (Python 3.11+) |
| **Base de datos** | MongoDB con motor asíncrono (Motor) |
| **ODM** | Beanie (Object Document Mapper basado en Pydantic, con hooks de serialización personalizados) |
| **Seguridad** | OAuth2 (JWT) + Passlib (Bcrypt) |
| **Despliegue** | Docker & Docker Compose (Arquitectura Multicontenedor) |
| **Testing** | Pytest, HTTPX y Pytest-Asyncio |

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
tests/           # Batería de pruebas automatizadas y aisladas
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

> Todos los endpoints privados requieren el token JWT en la cabecera `Authorization: Bearer <token>`.

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

### Productividad (Eventos, Tareas, Listas y Horarios)

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/events/me` | Lista de eventos del usuario |
| `GET` | `/tasks/me` | Lista de tareas del usuario |
| `GET` | `/lists/my_lists` | Lista de agrupaciones de ítems del usuario |
| `GET` | `/schedules/` | Lista de horarios base del usuario |
| `GET` | `/schedules/{id}/blocks` | Lista de bloques de un horario específico |

### Ajustes

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/settings/my_settings` | Obtener configuración personalizada |

---

## Documentación Interactiva

La API incluye documentación autogenerada con **Swagger UI**, protegida por Basic Auth para prevenir accesos no autorizados.

- **URL:** http://localhost:8000/docs
- **Credenciales:** definidas en `SWAGGER_USER` y `SWAGGER_PASSWORD` del archivo `.env`

---

## Benchmark de Rendimiento: SQL vs MongoDB

Para determinar la base de datos más adecuada para el proyecto, se llevaron a cabo pruebas de carga y rendimiento con **Locust**, simulando tráfico real de usuarios concurrentes sobre ambas implementaciones.

### Resultados

| Métrica | SQL (PostgreSQL) | MongoDB | Ganador |
|---|---|---|---|
| **Velocidad de respuesta** | Línea base | ~3× más rápido | ✅ MongoDB |
| **Tasa de fallos** | 7% | 1% | ✅ MongoDB |

### Conclusiones

MongoDB demostró una ventaja clara en ambas métricas críticas: triplicó la velocidad de respuesta bajo carga y redujo la tasa de errores del 7% al 1%. Estos resultados justifican la elección de MongoDB como base de datos definitiva del proyecto.

> La implementación SQL se conserva en la rama `sql` del repositorio para consulta y comparación.

---

## Testing y Calidad del Código

Se ha implementado una estrategia de pruebas exhaustiva con **pytest**, superando una batería de **33 tests automatizados** que validan:

- Flujo completo de registro y autenticación (Happy Path & Sad Path).
- Operaciones CRUD seguras y aisladas en Tareas, Eventos, Listas y Horarios.
- Borrado en cascada: Garantía de integridad de datos al eliminar entidades padre (ej. Horarios y sus bloques).
- Protección contra accesos no autorizados (Error 401 y 403).
- Validación estricta de esquemas Pydantic (Error 422).
- Ejecución determinista: Entornos de prueba aislados con limpieza de volúmenes en Docker para evitar falsos negativos.

### Ejecutar los tests

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

Al finalizar, se genera automáticamente un reporte de cobertura en formato HTML navegable disponible en `htmlcov/index.html`.

---

*Desarrollado por Paula — Proyecto TFG 2026*