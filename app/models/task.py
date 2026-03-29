from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id_fast

class TaskBase(BaseModel):
    # Define la estructura básica de una tarea.
    # Contiene la información fundamental que toda tarea debe tener.
    title: str # Título obligatorio
    description: Optional[str] = None # Descripción opcional

    # Por defecto, una tarea recién creada no está completada.
    # Al poner False, el cliente no necesita enviar este campo al crearla.
    completed: bool = False

    # Índice normal para user_id (SIN unique=True).
    # Esto es vital porque permite crear una relación de "1 a Muchos".
    # Acelera muchísimo las búsquedas tipo: "Tráeme todas las tareas del usuario 5".
    user_id: Indexed(int)

class Task(Document, TaskBase):
    # Este es el modelo real que Beanie guardará en MongoDB.
    # Hereda todo lo de TaskBase y le añade el comportamiento de base de datos.
    # Reemplazamos el ObjectId alfanumérico de Mongo por nuestro ID numérico
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        # Los documentos se guardarán en la colección "tasks"
        name = "tasks"

    # Gancho que se ejecuta automáticamente antes de hacer un ".insert()"
    @before_event(Insert)
    def assign_id(self):
        # Le asigna el siguiente ID numérico disponible a la tarea
        # justo antes de guardarla por primera vez.
        if self.id is None:
            self.id = get_next_id_fast()

class TaskCreate(TaskBase):
    # Esquema que recibe FastAPI cuando el cliente envía un POST para crear una tarea.
    # Requiere obligatoriamente 'title' y 'user_id'.
    pass

class TaskUpdate(BaseModel):
    # Esquema para cuando el cliente quiere editar una tarea (PATCH).
    # Aquí no incluimos el 'user_id'. De esta forma evitamos que un usuario intente transferir
    # su tarea a otro usuario enviando un user_id diferente en la actualización.
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None # Muy útil para hacer el "check" o "uncheck" de la tarea

class TaskOut(TaskBase):
    # Esquema que FastAPI devuelve al cliente web o móvil.
    # Hacemos que el ID sea obligatorio en la respuesta para que el frontend
    # sepa qué tarea es y pueda editarla o borrarla después.
    id: int

    # Permite transformar el Documento de Beanie a un JSON limpio de salida
    model_config = ConfigDict(from_attributes=True)