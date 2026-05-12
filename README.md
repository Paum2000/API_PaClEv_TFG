# PaClEv API

API robusta y asíncrona desarrollada para el Trabajo de Fin de Grado **PaClEv**. Construida con FastAPI, arquitectura NoSQL (MongoDB) y contenedorizada con Docker para un despliegue ágil y reproducible.

> **Nota sobre las ramas del repositorio:** Este repositorio cuenta con dos ramas principales — `sql` y `mongo` — resultado de un estudio comparativo de rendimiento realizado con Locust. Tras las pruebas, MongoDB fue seleccionado como base de datos definitiva. Los resultados del benchmark están documentados más abajo.

---

## Funcionalidades Principales

| Módulo | Descripción |
|---|---|
| **Usuarios** | Registro, login y gestión de perfil seguro con sistema de puntos y gamificación. |
| **Autenticación** | Login stateless con tokens JWT y contraseñas encriptadas (Bcrypt). |
| **Social y Grupos** | Gestión de amistades y Grupos Colaborativos. Permite compartir recursos (tareas, eventos, listas) con control estricto de roles. |
| **Horarios** | Gestión de horarios semanales individuales o compartidos por grupo. Bloques de actividades personalizados. |
| **Eventos** | CRUD de eventos con soporte para recurrencia y sincronización grupal mediante `group_id`. |
| **Tareas** | Gestión de tareas con seguimiento de estado. Soporta tareas privadas y de grupo. La finalización otorga puntos (máximo 100/día). |
| **Listas** | Creación de listas de ítems (ej. compra, notas) con opción de colaboración en tiempo real dentro de grupos. |
| **Tienda** | Sistema de recompensas donde el usuario canjea sus puntos por Temas y Colores de acento personalizados. |
| **Ajustes** | Personalización de interfaz (idioma, colores, temas) basada en el inventario del usuario. |

---

## Stack Tecnológico

| Categoría | Tecnología |
|---|---|
| Framework backend | FastAPI (Python 3.11+) |
| Base de datos | MongoDB con motor asíncrono (Motor) |
| ODM | Beanie (Object Document Mapper con soporte para validación Pydantic v2) |
| Seguridad | OAuth2 (JWT) + Passlib (Bcrypt) + ABAC (Attribute-Based Access Control) |
| Despliegue | Docker & Docker Compose (Arquitectura Multicontenedor) |
| Testing | Pytest, HTTPX, Pytest-Asyncio y Coverage.py |

---

## Arquitectura del Sistema

El proyecto sigue el patrón de **Clean Architecture** para garantizar la separación de responsabilidades y la escalabilidad del código:

```
app/
├── models/      # Documentos MongoDB (Modelos "aplanados" para máxima compatibilidad con Beanie)
├── schemas/     # Modelos de validación Pydantic v2 (incluye soporte para group_id)
├── routers/     # Endpoints con inyección de dependencias de seguridad (verify_group_access)
├── services/    # Lógica de negocio (Gamificación, Tienda y validaciones grupales)
└── core/        # Seguridad JWT y centralización de escudos de acceso
tests/           # Suite de pruebas automatizadas y aisladas
```

---

## Puesta en Marcha

### 1. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

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

```bash
docker-compose up --build
```

La API estará disponible en: `http://localhost:25011`

---

## Endpoints Principales

### Social y Grupos (Colaboración)

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/groups/` | Crear un nuevo grupo (auto-admin) |
| `GET` | `/groups/{group_id}/members` | Listar miembros del grupo |
| `POST` | `/groups/{group_id}/members` | Añadir miembro (Solo Admin) |
| `GET` | `/events/group/{group_id}` | **[NUEVO]** Ver eventos compartidos del grupo |
| `GET` | `/tasks/group/{group_id}` | **[NUEVO]** Ver tareas compartidas del grupo |
| `GET` | `/lists/group/{group_id}` | **[NUEVO]** Ver listas compartidas del grupo |
| `GET` | `/schedules/group/{group_id}` | **[NUEVO]** Ver horarios compartidos del grupo |

### Tienda e Inventario

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/store/my-inventory` | Temas y colores desbloqueados |
| `POST` | `/store/buy-theme/{id}` | Canjear puntos por tema (Validación de saldo) |
| `POST` | `/store/buy-color` | Canjear 100 puntos por color de acento |

### Autenticación y Usuarios

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/auth/login` | Login y generación de JWT |
| `POST` | `/users/` | Registro de usuario |
| `GET` | `/users/me` | Perfil actual y saldo de puntos |

### Productividad y Ajustes

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/events/me` | Lista de eventos del usuario |
| `GET` | `/tasks/me` | Lista de tareas (completarlas suma +10 puntos) |
| `GET` | `/lists/my_lists` | Lista de agrupaciones de ítems del usuario |
| `GET` | `/schedules/` | Lista de horarios base del usuario |
| `GET` | `/settings/my_settings` | Obtener configuración estética activa |

---

## Testing y Calidad del Código

Se ha implementado una estrategia de pruebas exhaustiva, superando una batería de **más de 45 tests automatizados** con un **92% de cobertura**:

- **Seguridad Colaborativa:** Implementación de la dependencia `verify_group_access` que blinda los recursos compartidos mediante Error `403` (Forbidden) ante accesos no autorizados.
- **Validación de Flujos:** Tests específicos para el ciclo de vida de tareas, eventos y listas (Privado vs Compartido).
- **Gamificación Pro:** Validación de suma de puntos (+10/tarea) y flujo completo de compra en la tienda (Happy/Sad Paths).
- **Robustez:** Gestión de errores Pydantic (`422`), recursos no encontrados (`404`) y prevención de duplicados en grupos.

### Ejecutar tests y reporte de cobertura

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

---

*Desarrollado por Paula — Proyecto TFG 2026*