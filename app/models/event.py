from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# --- 1. CLASE BASE (El "Plano" o Template) ---
# Sirve para definir los campos comunes y no repetir código (DRY).
# No se usa directamente para crear tablas ni para validar endpoints.
class EventBase(SQLModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: bool = False
    is_recurring: bool = False
    recurrence: Optional[str] = None
    color: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")

# --- 2. MODELO DE TABLA (La Base de Datos) ---
# Esta clase representa la tabla real en SQL ("events").
# Hereda de EventBase para tener todos los campos, pero añade el ID y la Relación.
class Event(EventBase, table=True):
    __tablename__ = "events"
    # El ID es opcional aquí porque al crear el objeto aún no existe en la DB (se genera solo)
    id: Optional[int] = Field(default=None, primary_key=True)

    # Define la conexión con el modelo User (quién es el dueño del evento)
    owner: Optional["User"] = Relationship(back_populates="events")

# --- 3. MODELO DE CREACIÓN (Input del Usuario) ---
# Se usa en el POST. Sirve para que el usuario envíe los datos.
# Por ahora es igual a EventBase, pero podrías quitar campos que no quieres que
# el usuario defina manualmente (como un campo 'created_at').
class EventCreate(EventBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (PATCH) ---
# Aquí TODOS los campos son opcionales (Optional).
# Sirve para que, si el usuario solo quiere cambiar el 'title',
# no esté obligado a enviar de nuevo los datos.
class EventUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    is_recurring: Optional[bool] = None
    recurrence: Optional[str] = None
    color: Optional[str] = None

# --- 5. MODELO DE SALIDA (Output de la API) ---
# Es lo que la API responde al cliente (JSON).
# Incluye el 'id' (que ya no es opcional porque viene de la DB).
# Protege tu base de datos al no enviar información sensible si la hubiera.
class EventOut(EventBase):
    id: int