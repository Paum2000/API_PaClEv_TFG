from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional
# Importamos la base original desde tus esquemas
from app.schemas.task import TaskBase

class Task(Document, TaskBase):
    # Clave primaria de Mongo
    id: Optional[int] = Field(default=None, alias="_id")

    # Índice para acelerar las búsquedas por usuario
    user_id: Indexed(int)

    class Settings:
        name = "tasks"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()
