import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.setting import settings

# Importamos todos los modelos de base de datos que Beanie necesita gestionar.
from app.models.event import Event
from app.models.setting import Setting
from app.models.task import Task
from app.models.theme import Theme
from app.models.user import User
from app.models.list import UserList


# A veces, ciertas versiones de Motor/PyMongo chocan con características
# internas de Beanie al intentar añadir metadatos. Esta línea es un "salvavidas"
# que previene errores al iniciar la aplicación si esa función no existe.
if not hasattr(AsyncIOMotorClient, 'append_metadata'):
    AsyncIOMotorClient.append_metadata = lambda self, *args, **kwargs: None


async def init_db():
    # Función asíncrona que se ejecuta al arrancar FastAPI para establecer
    # el "pool" de conexiones con MongoDB y registrar los modelos de Beanie.
    # Toma la URL de las variables de entorno. Si no la encuentra, usa localhost por defecto.
    mongo_url = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")

    # En lugar de abrir y cerrar una conexión por cada usuario, Mongo mantiene
    # un grupo de conexiones abiertas listas para usarse.
    client = AsyncIOMotorClient(
        mongo_url,
        maxPoolSize=1000, # Permite hasta 1000 operaciones concurrentes. Ideal para alta carga.
        minPoolSize=100,  # Mantiene siempre 100 conexiones vivas para responder inmediatamente a los primeros usuarios.
        serverSelectionTimeoutMS=10000, # Si MongoDB se cae, la app espera 10s antes de dar error.
        waitQueueTimeoutMS=20000 # Si las 1000 conexiones están ocupadas, el usuario #1001 espera máximo 20s en la fila.
    )

    # Selecciona la base de datos específica basándose en tus configuraciones (settings)
    database = client[settings.database_name]


    # Aquí le decimos a Beanie: "Revisa estas clases de Python,
    # conéctalas a las colecciones de la base de datos y prepara sus índices".
    await init_beanie(
        database=database,
        document_models=[
            User,
            Event,
            Theme,
            Task,
            Setting,
            UserList
        ]
    )