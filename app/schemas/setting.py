from pydantic import BaseModel
from typing import Optional

class SettingBase(BaseModel):
    accent_color: Optional[str] = None
    lenguaje: str = "es"

class SettingCreate(SettingBase):
    user_id: int
    theme_id: int

class SettingOut(SettingBase):
    id: int
    user_id: int
    theme_id: int
    class Config:
        from_attributes = True

class SettingUpdate(BaseModel):
    theme_id: Optional[int] = None
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None