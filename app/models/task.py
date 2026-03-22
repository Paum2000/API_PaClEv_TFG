from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# --- 1. CLASE BASE (Definición de la Tarea) ---
# Aquí defines qué es una "Tarea" en tu sistema.
# Se usa como molde para que todas las demás clases compartan estos campos.
class TaskBase(SQLModel):
    title: str                      # Título de la tarea (obligatorio)
    description: Optional[str] = None # Detalle opcional
    start_date: datetime            # Cuándo empieza o se crea
    done_date: Optional [datetime] = None # Fecha límite o de finalización
    done: bool = False              # Estado: ¿está terminada? (por defecto No)
    color: Optional[str] = None     # Etiqueta visual
    priority: str = "Media"         # Nivel de importancia (Baja, Media, Alta)
    user_id: int = Field(foreign_key="users.id") # El dueño de la tarea

# --- 2. MODELO DE TABLA (Base de Datos) ---
# Esta es la clase que crea la tabla física "tasks" en la base de datos.
class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    # El ID es la llave primaria. Es Optional porque la DB lo genera automáticamente.
    id: Optional[int] = Field(default=None, primary_key=True)

    # RELACIÓN: Permite acceder al objeto 'User' que creó la tarea.
    # Ejemplo: mi_tarea.owner.username devolvería el nombre del usuario.
    owner: Optional["User"] = Relationship(back_populates="tasks")

# --- 3. MODELO DE CREACIÓN (Input) ---
# Se usa cuando el usuario envía una nueva tarea desde el frontend.
# Por ahora es igual a Tast, pero podrías quitar campos que no quieres que
# el usuario defina manualmente.
class TaskCreate(TaskBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (Edición Parcial) ---
# Permite marcar una tarea como "hecha" (done: True)
# sin tener que volver a enviar todo.
# Todos los campos son Optional para permitir cambios mínimos.
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: Optional[bool] = None
    color: Optional[str] = None
    priority: Optional[str] = None

# --- 5. MODELO DE SALIDA (Respuesta de la API) ---
# Es lo que el cliente recibe de vuelta.
# Incluye el 'id' obligatoriamente para que el frontend sepa a qué tarea
# referirse en futuras ediciones o eliminaciones.
class TaskOut(TaskBase):
    id: int