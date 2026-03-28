from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

# Importamos la función para generar IDs numéricos
from app.models.counter import get_next_id

# --- 1. CLASE BASE (Identidad del Usuario) ---
# Contiene los datos públicos o generales. Usamos BaseModel de Pydantic.
class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

# --- 2. MODELO DE TABLA (La Colección en Mongo) ---
# Aquí se guarda la información sensible.
class User(Document, UserBase):
    # ID numérico autoincremental para identificar a cada usuario.
    id: Optional[int] = Field(default=None)

    # Sobrescribimos el email para decirle a Mongo que cree un índice único.
    # Esto acelera las búsquedas y evita correos duplicados, igual que 'unique=True, index=True'
    email: Indexed(EmailStr, unique=True)

    # Guardar el 'hash', nunca la contraseña real por seguridad.
    password_hash: str

    class Settings:
        name = "users" # Equivalente a __tablename__ = "users"

    # Generador automático del ID numérico al insertar
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            self.id = await get_next_id("users_id")

# --- 3. MODELO DE CREACIÓN (Registro) ---
# Cuando alguien se registra, envía su contraseña en texto plano ('password').
class UserCreate(UserBase):
    password: str

# --- 4. MODELO DE ACTUALIZACIÓN (Perfil) ---
# Permite al usuario cambiar su nombre, foto o contraseña de forma independiente.
class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None # Para cambio de contraseña
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

# --- 5. MODELO DE SALIDA (Respuesta de la API) ---
# Esto garantiza que la API nunca envíe la contraseña ni datos críticos al frontend.
class UserOut(UserBase):
    id: int

    # Equivalente en Pydantic v2 a la configuración orm_mode para leer de la BD
    model_config = ConfigDict(from_attributes=True)