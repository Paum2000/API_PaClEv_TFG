from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.counter import get_next_id_fast

class UserBase(BaseModel):
    # Define los campos públicos o comunes del usuario.
    # Aquí no incluimos la contraseña por seguridad.
    user_name: str

    # EmailStr es una maravilla de Pydantic: valida automáticamente que
    # el texto tenga formato real de correo (ej: usuario@dominio.com).
    email: EmailStr

    birthday: Optional[datetime] = None

    # Aquí puedes guardar la URL de la foto de perfil
    user_photo: Optional[str] = None

class User(Document, UserBase):
    # El documento real que se guarda en MongoDB.
    # Reemplazamos el _id de Mongo por nuestro int autoincremental
    id: Optional[int] = Field(default=None, alias="_id")

    # Sobrescribimos el campo 'email' de UserBase para decirle a Beanie:
    # 1. Crea un índice para buscar usuarios por email rapidísimo (útil para el login).
    # 2. unique=True: Imposibilitando que dos usuarios se registren con el mismo email.
    email: Indexed(EmailStr, unique=True)

    # Este campo es exclusivo de la base de datos.
    # Aquí guardamos la contraseña encriptada (hasheada), nunca en texto plano.
    password_hash: str

    class Settings:
        name = "users"

    # Gancho para asignar el ID numérico único antes de crear el usuario
    @before_event(Insert)
    def assign_id(self):
        if self.id is None:
            self.id = get_next_id_fast()

class UserCreate(UserBase):
    # Esquema que recibe FastAPI cuando el usuario llena el formulario de registro (POST).
    # Hereda de UserBase (pide nombre, email, etc.) y añade la contraseña en texto plano
    # para recibirla y luego encriptarla y pasarla al modelo 'User'.
    password: str

class UserUpdate(BaseModel):
    # Esquema para editar el perfil (PATCH).
    # Todo es opcional. Incluye 'password' por si el usuario quiere cambiar su contraseña,
    # en cuyo caso tu backend tendrá que detectarlo y volver a hashearla.
    user_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

class UserOut(UserBase):
    # Esquema de respuesta de la API (GET perfil, respuesta tras registro, etc.).
    # Como hereda de UserBase, devuelve el nombre, el email y la foto,
    # pero OMITE por completo el 'password_hash' (que está en User) y el 'password'
    # (que está en UserCreate). Así jamás filtramos la contraseña al frontend.
    id: int # El ID es público y necesario para el frontend

    model_config = ConfigDict(from_attributes=True)