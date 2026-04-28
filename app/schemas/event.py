from pydantic import BaseModel, ConfigDict, Field, PlainSerializer
from datetime import date, time
from typing import Optional, Annotated


class EventBase(BaseModel):
    # Contiene todos los campos comunes que definen cómo es un evento
    # en la aplicación.
    title: str
    description: Optional[str] = None
    start_date: date                       # Qué día empieza
    start_time: Optional[time] = None      # A qué hora
    end_date: Optional[date] = None        # Qué día termina
    end_time: Optional[time] = None        # A qué hora termina

    # Banderas lógicas, útiles para el frontend
    is_all_day: bool = False
    is_recurring: bool = False

    # Aquí guardamos una regla RRULE (ej: "FREQ=WEEKLY;BYDAY=MO")
    # si usamos estándares de calendario.
    recurrence: Optional[str] = None

    # Para la personalización visual en la app (ej: "#FF0000")
    color: Optional[str] = None

class EventCreate(EventBase):
    # Se usa cuando el cliente envía una petición POST para crear un evento.
    # Hereda todo lo de EventBase y añade el 'user_id' de forma obligatoria.
    user_id: int

class EventOut(EventBase):
    # Es lo que FastAPI le devuelve al frontend.
    id: int = Field(alias="_id") # El ID autoincremental generado por Mongo/Beanie
    user_id: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class EventUpdate(BaseModel):
    # Se usa cuando el usuario quiere editar un evento existente.
    # Todo es opcional (Optional) para permitir que cambie solo una cosa
    # (ej: cambiar solo el color) sin tener que enviar toda la fecha de nuevo.
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    start_time: Optional[time] = None
    end_date: Optional[date] = None
    end_time: Optional[time] = None
    is_all_day: Optional[bool] = None
    is_recurring: Optional[bool] = None
    recurrence: Optional[str] = None
    color: Optional[str] = None
