from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# --- 1. CLASE BASE (Identidad del Usuario) ---
# Contiene los datos públicos o generales.
class UserBase(SQLModel):
    user_name: str
    # 'unique=True' asegura que no haya dos personas con el mismo correo.
    # 'index=True' acelera las búsquedas cuando el usuario inicia sesión.
    email: str = Field(unique=True, index=True)
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

# --- 2. MODELO DE TABLA (La Base de Datos) ---
# Aquí se guarda la información sensible de la DB.
class User(UserBase, table=True):
    __tablename__ = "users"
    # ID autoincremental para identificar a cada usuario.
    id: Optional[int] = Field(default=None, primary_key=True)

    #Guardar el 'hash', nunca la contraseña real por seguridad.
    password_hash: str

    # RELACIONES :
    # 'List' indica que un usuario puede tener MUCHAS tareas y MUCHOS eventos.
    tasks: List["Task"] = Relationship(back_populates="owner")
    events: List["Event"] = Relationship(back_populates="owner")

    # 'Optional' indica que un usuario tiene solo UNA configuración (o ninguna al inicio).
    settings: Optional["Setting"] = Relationship(back_populates="user")

# --- 3. MODELO DE CREACIÓN (Registro) ---
# Cuando alguien se registra, envía su contraseña en texto plano ('password').
# Luego, la convertimos en 'password_hash' para el modelo User.
class UserCreate(UserBase):
    password: str

# --- 4. MODELO DE ACTUALIZACIÓN (Perfil) ---
# Permite al usuario cambiar su nombre, foto o contraseña de forma independiente.
class UserUpdate(SQLModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None # Para cambio de contraseña
    birthday: Optional[datetime] = None
    user_photo: Optional[str] = None

# --- 5. MODELO DE SALIDA (Respuesta de la API) ---
# Esto garantiza que tu API nunca envíe la contraseña ni datos criticos al frontend.
class UserOut(UserBase):
    id: int