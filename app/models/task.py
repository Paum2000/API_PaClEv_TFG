from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.counter import get_next_id

# --- 1. CLASE BASE (Atributos comunes) ---
# Extraemos todos los campos que se repiten constantemente.
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    priority: str = "Media"
    user_id: int  # Referencia al usuario dueño de la tarea

# --- 2. MODELO DE COLECCIÓN (La Base de Datos en Mongo) ---
# Hereda todos los campos de TaskBase y le añade el ID y el estado 'done'.
class Task(Document, TaskBase):
    id: Optional[int] = Field(default=None)
    done: bool = False

    class Settings:
        name = "tasks"

    # Generador automático del ID numérico al insertar
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            self.id = await get_next_id("tasks_id")

# --- 3. MODELO DE CREACIÓN (POST) ---
# Como al crear una tarea enviamos exactamente los datos de la base,
# usamos 'pass'. El campo 'done' no hace falta porque por defecto será False.
class TaskCreate(TaskBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (PUT) ---
# Va por libre porque todos sus campos deben ser opcionales para
# permitir actualizaciones parciales (ej: solo cambiar el título).
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: Optional[bool] = None
    priority: Optional[str] = None

# --- 5. MODELO DE SALIDA (Respuesta GET de la API) ---
# Hereda de TaskBase y añade los campos guardados en la base de datos.
class TaskOut(TaskBase):
    id: int
    done: bool

    model_config = ConfigDict(from_attributes=True)