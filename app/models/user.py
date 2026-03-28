from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.counter import get_next_id_fast

class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

class User(Document, UserBase):
    id: Optional[int] = Field(default=None, alias="_id")
    email: Indexed(EmailStr, unique=True)
    password_hash: str

    class Settings:
        name = "users"

    @before_event(Insert)
    def assign_id(self):
        if self.id is None:
            self.id = get_next_id_fast()

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

class UserOut(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)