from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.counter import get_next_id

# --- 1. CLASE BASE (Atributos comunes) ---
# Centralizamos los datos del evento que se repiten.
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: bool = False
    user_id: int # Relación con el usuario creador

# --- 2. MODELO DE COLECCIÓN (La Base de Datos en Mongo) ---
# Hereda de Document y de EventBase. Solo necesita añadir el ID y el Hook.
class Event(Document, EventBase):
    id: Optional[int] = Field(default=None)

    class Settings:
        name = "events"

    # Generador automático del ID numérico al insertar
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            self.id = await get_next_id("events_id")

# --- 3. MODELO DE CREACIÓN (POST) ---
# Como al crear un evento necesitamos los mismos datos que en la base,
# heredamos directamente usando 'pass'.
class EventCreate(EventBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (PUT) ---
# Todos los campos opcionales.
# Excluimos 'user_id' intencionadamente para que
# un usuario no pueda transferir la propiedad del evento a otra persona.
class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    is_all_day: Optional[bool] = None

# --- 5. MODELO DE SALIDA (Respuesta GET de la API) ---
# Hereda todos los detalles del evento y le añade el ID para que
# el Frontend sepa qué evento está pintando en el calendario.
class EventOut(EventBase):
    id: int

    model_config = ConfigDict(from_attributes=True)