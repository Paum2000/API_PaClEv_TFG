from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- 1. TASK BASE (El ADN de la Tarea) ---
# Define qué información compone una tarea.
# Nota: Aquí no incluimos 'user_id' porque la base solo describe la tarea en sí.
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    done_date: datetime
    done: bool = False              # Estado por defecto: no terminada.
    color: Optional[str] = None
    priority: str = "Media"         # Valor por defecto si no se envía nada.

# --- 2. TASK CREATE (Entrada de datos) ---
# Se usa cuando el usuario crea una tarea desde el Frontend.
# Aquí SÍ añadimos 'user_id' porque necesitamos saber a quién pertenece.
class TaskCreate(TaskBase):
    user_id: int

# --- 3. TASK OUT (Salida de datos) ---
# Lo que la API devuelve al Frontend.
class TaskOut(TaskBase):
    id: int        # El ID es vital para que el Frontend pueda editarla luego.
    user_id: int   # Confirmamos quién es el dueño.

    # Permite que Pydantic convierta automáticamente objetos de SQLModel a JSON.
    class Config:
        from_attributes = True

# --- 4. TASK UPDATE (Edición Parcial) ---
# Sirve para marcar una tarea como 'done' sin reenviar el título o las fechas
# o editar algun campo.
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: Optional[bool] = None
    color: Optional[str] = None
    priority: Optional[str] = None