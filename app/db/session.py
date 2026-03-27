from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.setting import settings
from app.models.counter import Counter
from app.models.event import Event
from app.models.setting import Setting
from app.models.task import Task
from app.models.theme import Theme
from app.models.user import User

async def init_db():
    # 1. Creamos el cliente asíncrono apuntando a tu MongoDB local
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    # 2. Seleccionamos la base de datos
    database = client[settings.database_name]

    # 3. Inicializamos Beanie con los modelos que representan nuestras colecciones
    await init_beanie(
        database=database,
        document_models=[
            Counter, User, Event, Theme, Task, Setting
        ]
    )