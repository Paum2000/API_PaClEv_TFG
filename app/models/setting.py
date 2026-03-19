from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class SettingBase(SQLModel):
    accent_color: Optional[str] = None
    lenguaje: str = "es"
    user_id: int = Field(foreign_key="users.id")
    theme_id: int = Field(foreign_key="themes.id")

class Setting(SettingBase, table=True):
    __tablename__ = "settings"
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional["User"] = Relationship(back_populates="settings")
    theme: Optional["Theme"] = Relationship(back_populates="settings")

class SettingCreate(SettingBase):
    pass

class SettingUpdate(SQLModel):
    theme_id: Optional[int] = None
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None

class SettingOut(SettingBase):
    id: int