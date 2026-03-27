from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.counter import get_next_id


class User(Document):
    id: Optional[int] = Field(default=None)
    user_name: str
    email: Indexed(EmailStr, unique=True)
    password_hash: str
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

    class Settings:
        name = "users"

    # Justo antes de hacer un .insert(), Beanie ejecutará esta función
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            # Llama al contador pidiendo el siguiente número para la colección 'events'
            self.id = await get_next_id("events_id")

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    birthday: Optional[datetime] = None

class UserOut(BaseModel):
    id: int
    user_name: str
    email: EmailStr
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)