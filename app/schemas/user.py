from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# --- 1. USER BASE (El molde principal) ---
# Define los campos que casi siempre estarán presentes.
class UserBase(BaseModel):
    user_name: str
    # 'EmailStr' valida automáticamente si el texto tiene formato de correo real.
    email: EmailStr
    birthday: datetime
    user_photo: Optional[str] = None # Campo opcional (puede ser null)

# --- 2. USER CREATE (Registro de usuario) ---
# Se usa cuando alguien se registra.
# Hereda de UserBase pero añade la contraseña, que es obligatoria al crear.
class UserCreate(UserBase):
    password: str

# --- 3. USER OUT (Lo que la API responde) ---
# Es lo que el mundo ve. No inclulle datos personales ni la contraseña.
class UserOut(UserBase):
    id: int # El ID ya es obligatorio porque viene de la DB.

    # Esta configuración permite que Pydantic lea datos directamente
    # de objetos de SQLModel o SQLAlchemy.
    class Config:
        from_attributes = True

# --- 4. USER UPDATE (Edición de perfil) ---
# Esta clase es para peticiones tipo PATCH.
# Aquí no hereda de UserBase ya que en una actualización, todo debe ser opcional.
class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None # Permite cambiar la clave si se envía
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None