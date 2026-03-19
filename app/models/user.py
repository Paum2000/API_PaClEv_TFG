from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    user_name: str
    email: str = Field(unique=True, index=True)
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str

    # Relaciones
    tasks: List["Task"] = Relationship(back_populates="owner")
    events: List["Event"] = Relationship(back_populates="owner")
    settings: Optional["Setting"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

class UserOut(UserBase):
    id: int