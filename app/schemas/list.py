from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List as PyList

class ListBase(BaseModel):
    name: str
    items: PyList[str] = []

class ListCreate(ListBase):
    pass

class ListOut(ListBase):
    id: int = Field(alias="_id")
    user_id: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class ListUpdate(BaseModel):
    # Todo opcional para los métodos PUT/PATCH
    name: Optional[str] = None
    items: Optional[PyList[str]] = None