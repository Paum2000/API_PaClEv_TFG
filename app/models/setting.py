from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from app.models.counter import get_next_id


class Setting(Document):
    id: Optional[int] = Field(default=None)
    accent_color: str = "#000000"
    lenguaje: str = "es"
    user_id: int
    theme_id: int

    class Settings:
        name = "settings"

    # Justo antes de hacer un .insert(), Beanie ejecutará esta función
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            # Llama al contador pidiendo el siguiente número para la colección 'events'
            self.id = await get_next_id("settings_id")

class SettingCreate(BaseModel):
    accent_color: Optional[str] = "#000000"
    lenguaje: Optional[str] = "es"
    user_id: int
    theme_id: int

class SettingUpdate(BaseModel):
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None
    theme_id: Optional[int] = None

class SettingOut(BaseModel):
    id: int
    accent_color: str
    lenguaje: str
    user_id: int
    theme_id: int

    model_config = ConfigDict(from_attributes=True)