from pydantic import BaseModel
from typing import Optional

class ThemeBase(BaseModel):
    name: str

class ThemeCreate(ThemeBase):
    pass

class ThemeOut(ThemeBase):
    id: int
    class Config:
        from_attributes = True

class ThemeUpdate(BaseModel):
    name: Optional[str] = None