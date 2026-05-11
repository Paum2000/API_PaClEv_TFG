from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional
# Importamos la base desde tus esquemas
from app.schemas.inventory import InventoryBase

class UserInventory(Document, InventoryBase):
    # Tu sistema de IDs autoincrementales
    id: Optional[int] = Field(default=None, alias="_id")

    # Guardamos de quién es el objeto y le ponemos un índice (Indexed)
    # para que cuando el usuario abra su inventario, la búsqueda sea ultrarrápida.
    user_id: Indexed(int)

    class Settings:
        name = "user_inventory"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()