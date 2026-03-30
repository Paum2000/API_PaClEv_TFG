from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    # Define los campos de perfil del usuario.
    user_name: str

    # EmailStr es una herramienta fantástica. FastAPI rechazará automáticamente
    # la petición (Error 422) si el usuario envía "hola123" en lugar de "hola@email.com".
    email: EmailStr

    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

class UserCreate(UserBase):
    # Lo que la API exige cuando el usuario se registra en la app.
    # Hereda el nombre, email, etc., y le añado la contraseña obligatoria.
    password: str

class UserOut(UserBase):
    # Lo que FastAPI devuelve al cliente web/móvil.

    # Al heredar de UserBase, devuelve el ID, nombre, email y foto.
    # Como no hereda de UserCreate, la contraseña no existe aquí.
    id: Optional[int] = Field(None, alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class UserUpdate(BaseModel):
    # Esquema para cuando el usuario edita su perfil.
    # Todo es opcional.
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None