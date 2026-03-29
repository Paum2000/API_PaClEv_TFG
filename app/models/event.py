from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
# Importas la función que genera el ID autoincremental desde otro módulo
from app.models.counter import get_next_id_fast


class EventBase(BaseModel):
    # Define los campos principales que se usarán en casi todas las
    # variantes del modelo.
    title: str
    description: Optional[str] = None
    event_date: datetime
    # Indexed(int) le dice a MongoDB que cree un índice para acelerar
    # las búsquedas filtradas por el ID del usuario.
    user_id: Indexed(int)

class Event(Document, EventBase):
    # Este es el modelo que interactúa directamente con MongoDB.
    # Hereda los campos de EventBase y añade las configuraciones de Beanie.
    # Sobrescribimos el _id por defecto de Mongo (ObjectId) por un entero.
    # El alias="_id" es crucial para que MongoDB lo reconozca como su clave primaria.
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        # Define el nombre de la colección en la base de datos MongoDB
        name = "events"

    # Este "hook" se ejecuta automáticamente justo antes de insertar
    # un nuevo documento en la base de datos.
    @before_event(Insert)
    def assign_id(self):
        # Si el evento no tiene ID asignado al momento de guardarlo,
        # obtiene el siguiente ID autoincremental de la secuencia.
        if self.id is None:
            self.id = get_next_id_fast()


class EventCreate(EventBase):
    # Esquema utilizado para recibir los datos cuando el cliente hace un POST.
    # Por ahora es idéntico a EventBase, pero tenerlo separado permite
    # añadir campos en el futuro que solo sean necesarios al crear.
    pass

class EventUpdate(BaseModel):
    # Esquema utilizado para actualizar datos.
    # Todos los campos son opcionales para permitir que el
    # cliente envíe solo el dato específico que quiere cambiar.
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None

class EventOut(EventBase):
    # Esquema utilizado para enviar la respuesta al cliente (GET/POST/etc).
    # Hereda de EventBase y se asegura de incluir siempre el ID generado.
    id: int # Aquí el ID es obligatorio porque si sale de la DB, ya debe tener uno.

    # ConfigDict(from_attributes=True) permite que Pydantic lea los datos
    # directamente del objeto Document de Beanie/Mongo y los transforme a JSON.
    model_config = ConfigDict(from_attributes=True)