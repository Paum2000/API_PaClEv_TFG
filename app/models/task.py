from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id_fast

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    # Indexamos para que buscar tareas de un usuario sea ultra rápido
    user_id: Indexed(int)

class Task(Document, TaskBase):
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        name = "tasks"

    @before_event(Insert)
    def assign_id(self):
        if self.id is None:
            self.id = get_next_id_fast()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(TaskBase):
    id: int
    model_config = ConfigDict(from_attributes=True)