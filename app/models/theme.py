from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.models.counter import get_next_id


class Theme(Document):
    id: Optional[int] = Field(default=None)
    name: str

    class Settings:
        name = "themes"

    # Justo antes de hacer un .insert(), Beanie ejecutará esta función
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            # Llama al contador pidiendo el siguiente número para la colección 'events'
            self.id = await get_next_id("themes_id")

class ThemeCreate(BaseModel):
    name: str

class ThemeUpdate(BaseModel):
    name: Optional[str] = None

class ThemeOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)