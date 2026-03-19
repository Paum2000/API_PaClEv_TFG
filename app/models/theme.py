from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class ThemeBase(SQLModel):
    name: str

class Theme(ThemeBase, table=True):
    __tablename__ = "themes"
    id: Optional[int] = Field(default=None, primary_key=True)
    settings: List["Setting"] = Relationship(back_populates="theme")

class ThemeCreate(ThemeBase):
    pass

class ThemeUpdate(SQLModel):
    name: Optional[str] = None

class ThemeOut(ThemeBase):
    id: int