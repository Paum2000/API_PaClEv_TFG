from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
import os

# Importamos el motor
from app.db.session import engine

# Importamos los routers de nuestra agenda
from app.routers import users, tasks, events, themes, settings

app = FastAPI(title="PaClEv API")

# 1. Crear directorios para archivos estáticos (¡Ideal para user_photo!)
upload_dir = os.path.join("app", "static", "uploads")
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, exist_ok=True)

# 2. Montar la ruta estática
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 3. Incluir los routers
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(themes.router)
app.include_router(settings.router)

# 4. Inicializar la base de datos
def init_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    init_db()

