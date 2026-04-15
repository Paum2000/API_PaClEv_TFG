import os
import secrets
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.models.user import User
from app.core.security import get_password_hash

from app.db.session import init_db
from app.routers import users, tasks, events, themes, settings, auth

ADMIN_USER_NAME = os.getenv("FIRST_ADMIN_NAME", "admin")
ADMIN_EMAIL = os.getenv("FIRST_ADMIN_EMAIL", "admin@miproyecto.com")
ADMIN_PASSWORD = os.getenv("FIRST_ADMIN_PASSWORD", "admin1234")
ADMIN_NICKNAME = os.getenv("FIRST_ADMIN_NICKNAME","_admin_")

async def create_first_admin():

    # Buscamos si ya existe alguien con ese email
    admin_existente = await User.find_one(User.email == ADMIN_EMAIL)

    if not admin_existente:
        nuevo_admin = User(
            user_name=ADMIN_USER_NAME,
            nickname=ADMIN_NICKNAME,
            email=ADMIN_EMAIL,
            password_hash=get_password_hash(ADMIN_PASSWORD),
            is_admin=True
        )
        await nuevo_admin.insert()
        print(f"Admin creado automáticamente en BD: {ADMIN_EMAIL}")

# --- CICLO DE VIDA DE LA APLICACIÓN (Lifespan) ---
# Este gestor de contexto asíncrono reemplaza al antiguo @app.on_event("startup")
# y es la forma moderna (y sin DeprecationWarnings) de arrancar servicios en FastAPI.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Todo lo que ocurre ANTES del yield se ejecuta al encender el servidor.
    await init_db()
    await create_first_admin()
    yield # Aquí es cuando la API está encendida y recibiendo peticiones


# --- INICIALIZACIÓN DE FASTAPI ---
app = FastAPI(
    title="API PaClEv",
    description="Api con arquitectura NoSQL asíncrona",
    lifespan=lifespan,
    # DESACTIVAMOS LAS RUTAS PÚBLICAS POR DEFECTO
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# --- SEGURIDAD DE LA DOCUMENTACIÓN (Basic Auth) ---
security = HTTPBasic()

def verificar_admin_docs(credentials: HTTPBasicCredentials = Depends(security)):
    # Verifica las credenciales de la ventana emergente del navegador.
    es_usuario_correcto = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        ADMIN_NICKNAME.encode("utf-8")
    )
    es_password_correcta = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        ADMIN_PASSWORD.encode("utf-8")
    )

    if not (es_usuario_correcto and es_password_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado a la documentación",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Creamos las rutas manuales protegidas por la contraseña
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint(username: str = Depends(verificar_admin_docs)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

@app.get("/docs", include_in_schema=False)
async def get_swagger_ui(username: str = Depends(verificar_admin_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentación Admin - PaClEv")

# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (Fotos de perfil) ---
upload_dir = os.path.join("app", "static", "uploads")
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- REGISTRO DE ROUTERS ---
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(themes.router)
app.include_router(settings.router)
app.include_router(auth.router)

