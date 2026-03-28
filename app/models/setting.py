from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id_fast

class SettingBase(BaseModel):
    dark_mode: bool = False
    notifications_enabled: bool = True
    user_id: Indexed(int, unique=True) # Un usuario solo tiene una configuración

class Setting(Document, SettingBase):
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        name = "settings"

    @before_event(Insert)
    def assign_id(self):
        if self.id is None:
            self.id = get_next_id_fast()

class SettingCreate(SettingBase):
    pass

class SettingUpdate(BaseModel):
    dark_mode: Optional[bool] = None
    notifications_enabled: Optional[bool] = None

class SettingOut(SettingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)