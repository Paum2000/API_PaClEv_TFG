from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.counter import get_next_id


class Task(Document):
    id: Optional[int] = Field(default=None)
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: bool = False
    priority: str = "Media"
    user_id: int # Relación manual con User

    class Settings:
        name = "tasks"

    # Justo antes de hacer un .insert(), Beanie ejecutará esta función
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            # Llama al contador pidiendo el siguiente número para la colección 'events'
            self.id = await get_next_id("tasks_id")

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    priority: Optional[str] = "Media"
    user_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: Optional[bool] = None
    priority: Optional[str] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: bool
    priority: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)