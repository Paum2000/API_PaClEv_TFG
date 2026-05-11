# PaClEv API

> API robusta y asíncrona desarrollada para el Trabajo de Fin de Grado **PaClEv**.  
> Construida con **FastAPI**, arquitectura **NoSQL (MongoDB)** y contenedorizada con **Docker** para un despliegue ágil y reproducible.

---

> **Nota sobre las ramas del repositorio:** Este repositorio cuenta con dos ramas principales — `sql` y `mongo` — resultado de un estudio comparativo de rendimiento realizado con Locust. Tras las pruebas, **MongoDB fue seleccionado como base de datos definitiva**. Los resultados del benchmark están documentados más abajo.

---

## Funcionalidades Principales

| Módulo | Descripción |
|---|---|
| **Usuarios** | Registro, login y gestión de perfil seguro con sistema de puntos y gamificación. |
| **Autenticación** | Login stateless con tokens JWT y contraseñas encriptadas (Bcrypt). |
| **Social y Grupos** | Gestión de amistades bidireccional y creación de grupos colaborativos con control estricto de roles (Administrador/Miembro). |
| **Horarios** | Gestión de múltiples horarios semanales (ej. Verano/Invierno) con bloques de actividades personalizados por día y hora. |
| **Eventos** | CRUD de eventos con soporte avanzado para recurrencia y control independiente de fechas y horas. |
| **Tareas** | Gestión de tareas con seguimiento de estado. La finalización de tareas otorga puntos al usuario (máximo 100/día). |
| **Listas** | Creación y gestión de listas personalizadas de ítems aisladas por usuario. |
| **Tienda** | Sistema de recompensas donde el usuario canjea sus puntos por Temas y Colores de acento personalizados. |
| **Ajustes** | Personalización de interfaz (idioma, colores, temas) basada en el inventario del usuario. |

---

## Stack Tecnológico

| Categoría | Tecnología |
|---|---|
| Framework backend | FastAPI (Python 3.11+) |
| Base de datos | MongoDB con motor asíncrono (Motor) |
| ODM | Beanie (Object Document Mapper con soporte para validación Pydantic v2) |
| Seguridad | OAuth2 (JWT) + Passlib (Bcrypt) |
| Despliegue | Docker & Docker Compose (Arquitectura Multicontenedor) |
| Testing | Pytest, HTTPX, Pytest-Asyncio y Coverage.py |

---

## Arquitectura del Sistema

El proyecto sigue el patrón de **Clean Architecture** para garantizar la separación de responsabilidades y la escalabilidad del código:

```
app/
├── models/      # Definición de documentos MongoDB mediante Beanie
├── schemas/     # Modelos de validación de datos (entrada/salida) con Pydantic
├── routers/     # Endpoints y gestión de rutas HTTP
├── services/    # Lógica de negocio (Gamificación, Tienda y validaciones)
└── core/        # Configuraciones centrales, seguridad y variables de entorno
tests/           # Suite de pruebas automatizadas y aisladas
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

La API estará disponible en: **http://localhost:25011**

---

## Endpoints Principales

> Todos los endpoints privados requieren el token JWT en la cabecera `Authorization: Bearer <token>`.

### Social y Grupos

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/friends/request` | Enviar solicitud de amistad a un usuario |
| `POST` | `/friends/accept/{id}` | Aceptar una solicitud de amistad pendiente |
| `GET` | `/friends/My_friends` | Listar todos los amigos aceptados |
| `DELETE` | `/friends/{friend_id}` | Eliminar una relación de amistad |
| `POST` | `/groups/` | Crear un nuevo grupo (auto-asigna rol de administrador) |
| `GET` | `/groups/{group_id}/members` | Listar los miembros de un grupo |
| `POST` | `/groups/{group_id}/members` | Añadir un nuevo miembro al grupo (Solo Admin) |
| `DELETE` | `/groups/{group_id}/members/{user_id}` | Abandonar grupo o expulsar miembro (Solo Admin) |

### Tienda e Inventario

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/store/my-inventory` | Lista de temas y colores desbloqueados por el usuario |
| `POST` | `/store/buy-theme/{id}` | Canjear puntos por un nuevo tema visual |
| `POST` | `/store/buy-color` | Canjear puntos por un color de acento específico (Precio: 100 pts) |

### Autenticación y Usuarios

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/auth/login` | Inicio de sesión y generación de JWT |
| `POST` | `/users/` | Registro de nuevo usuario |
| `GET` | `/users/me` | Obtener datos del usuario actual (incluye saldo de puntos) |
| `PUT` | `/users/me` | Actualizar perfil |

### Productividad y Ajustes

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/events/me` | Lista de eventos del usuario |
| `GET` | `/tasks/me` | Lista de tareas (completarlas suma +10 puntos) |
| `GET` | `/lists/my_lists` | Lista de agrupaciones de ítems del usuario |
| `GET` | `/schedules/` | Lista de horarios base del usuario |
| `GET` | `/settings/my_settings` | Obtener configuración estética activa |

---

## Documentación Interactiva

La API incluye documentación autogenerada con **Swagger UI**, protegida por Basic Auth para prevenir accesos no autorizados.

- **URL:** http://localhost:8000/docs
- **Credenciales:** definidas en `SWAGGER_USER` y `SWAGGER_PASSWORD` del archivo `.env`

---

## Benchmark de Rendimiento: SQL vs MongoDB

| Métrica | SQL (PostgreSQL) | MongoDB | Ganador |
|---|---|---|---|
| Velocidad de respuesta | Línea base | ~3× más rápido | ✅ MongoDB |
| Tasa de fallos | 7% | 1% | ✅ MongoDB |

---

## Testing y Calidad del Código 

Se ha implementado una estrategia de pruebas exhaustiva, alcanzando un **93% de cobertura total de código** y superando una batería de **42 tests automatizados** que validan tanto los flujos de éxito (Happy Paths) como la tolerancia a fallos (Sad Paths):

- **Módulo Social:** Cobertura del 100% en la gestión de amistades y blindaje de la lógica de grupos (control de intrusos, prevención de duplicados, gestión de abandono/expulsión).
- **Flujo de Gamificación:** Validación de suma de puntos tras completar tareas y respeto del límite diario (100 pts/día).
- **Ciclo de Compra:** Simulación de ahorro y validación de saldo para adquisición de ítems (Temas y Colores).
- **Seguridad y Candados:** Verificación de que el usuario no puede equipar ítems que no posee en su inventario.
- **Integridad:** Borrado en cascada (ej. Horarios y sus bloques) y generación concurrente de IDs de alta precisión para evitar colisiones.
- **Validación:** Control estricto de esquemas Pydantic (Error 422) y accesos no autorizados (401/403/405).

### Ejecutar los tests y generar reporte de cobertura

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

Al finalizar, se genera automáticamente un reporte de cobertura en formato HTML navegable disponible en `htmlcov/index.html`.

---

*Desarrollado por **Paula** — Proyecto TFG 2026*