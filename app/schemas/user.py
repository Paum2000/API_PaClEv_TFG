from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    birthday: datetime
    user_photo: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None