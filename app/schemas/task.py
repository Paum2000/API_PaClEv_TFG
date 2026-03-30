from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    # Define los atributos que conforman una Tarea en el sistema.
    title: str
    description: Optional[str] = None

    # Control de tiempo.
    start_date: datetime
    done_date: Optional[datetime] = None

    # Por defecto, cuando creas una tarea, no está terminada.
    completed: bool = False

    # Personalización visual
    color: Optional[str] = None

    # Un detalle genial: Si el frontend no envía prioridad,
    # asumes "Media" automáticamente.
    priority: str = "Media"

class TaskCreate(TaskBase):
    # Lo que la API exige cuando el usuario envía el formulario de "Nueva Tarea".
    # Hereda todo lo anterior y hace obligatorio asociar la tarea a un usuario.
    user_id: int

class TaskOut(TaskBase):
    # Lo que FastAPI devuelve al cliente.
    id: int = Field(alias="_id")
    user_id: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class TaskUpdate(BaseModel):
    # Esquema exclusivo para modificar una tarea existente.
    # Todo es opcional para que el usuario pueda, por ejemplo,
    # solo marcar "done=True" sin reenviar todos los demás datos.
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime]=None
    done_date: Optional[datetime]=None
    completed: Optional[bool] = None