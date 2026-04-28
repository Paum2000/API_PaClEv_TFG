from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional
from app.schemas.list import ListBase

class UserList(Document, ListBase):
    # Usamos tu sistema de IDs numéricos
    id: Optional[int] = Field(default=None, alias="_id")

    # Índice para búsquedas rápidas, pero NO unique, porque un usuario tendrá varias listas
    user_id: Indexed(int)

    class Settings:
        name = "user_lists"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()