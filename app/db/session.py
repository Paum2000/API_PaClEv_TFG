import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.setting import settings

from app.models.counter import Counter
from app.models.event import Event
from app.models.setting import Setting
from app.models.task import Task
from app.models.theme import Theme
from app.models.user import User


if not hasattr(AsyncIOMotorClient, 'append_metadata'):
    AsyncIOMotorClient.append_metadata = lambda self, *args, **kwargs: None


async def init_db():
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_url)

    database = client[settings.database_name]

    await init_beanie(
        database=database,
        document_models=[
            Counter, User, Event, Theme, Task, Setting
        ]
    )