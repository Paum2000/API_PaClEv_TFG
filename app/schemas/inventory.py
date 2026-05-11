from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class InventoryBase(BaseModel):
    # ¿Qué tipo de objeto ha comprado? (Ej: "THEME", "COLOR")
    item_type: str

    # Referencia al objeto (Ej: el ID del tema "5", o un color "#FF0000")
    item_reference: str

class InventoryCreate(InventoryBase):
    # Esquema para cuando se registra la compra internamente.
    pass

class InventoryOut(InventoryBase):
    # Lo que la API devuelve cuando el móvil pide "mi inventario".
    id: int = Field(alias="_id")
    user_id: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

