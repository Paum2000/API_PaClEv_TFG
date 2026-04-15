from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict, EmailStr
from typing import Optional
# Importamos la base desde tus esquemas
from app.schemas.user import UserBase

class User(Document, UserBase):
    id: Optional[int] = Field(default=None, alias="_id")

    # Beanie necesita saber que el email es único e indexado
    email: Indexed(EmailStr, unique=True)
    nickname: Indexed(str, unique=True)

    # Campos exclusivo de la BD
    password_hash: str
    is_admin: bool = False

    class Settings:
        name = "users"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()