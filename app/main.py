import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.session import init_db
from app.routers import users, tasks, events, themes, settings

# --- CICLO DE VIDA DE LA APLICACIÓN (Lifespan) ---
# Este gestor de contexto asíncrono reemplaza al antiguo @app.on_event("startup")
# y es la forma moderna (y sin DeprecationWarnings) de arrancar servicios en FastAPI.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Todo lo que ocurre ANTES del yield se ejecuta al encender el servidor.
    await init_db()
    yield # Aquí es cuando la API está encendida y recibiendo peticiones


# --- INICIALIZACIÓN DE FASTAPI ---
app = FastAPI(
    title="API PaClEv",
    description="Api con arquitectura NoSQL asíncrona",
    lifespan=lifespan
)

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

