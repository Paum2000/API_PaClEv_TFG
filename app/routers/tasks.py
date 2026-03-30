from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service

# Todas las rutas de este archivo tendrán el prefijo "/tasks"
# y se agruparán bajo la etiqueta "Tasks" en la documentación de Swagger.
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# response_model=TaskOut: Nos asegura que el frontend recibirá el 'id' generado.
@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate):
    # Recibe el esquema TaskCreate (exige title y user_id)
    # y lo envía al servicio para guardarlo en la base de datos.
    return await task_service.create_task(task)

# response_model=List[TaskOut]: Crucial aquí. Le indica a FastAPI que
# la respuesta será un arreglo (array) de múltiples tareas.
@router.get("/user/{user_id}", response_model=List[TaskOut])
async def get_user_tasks(user_id: int):
    # Busca todas las tareas asociadas a un usuario en particular.
    # Como pusimos un índice (Indexed) en user_id en el modelo de base de datos,
    # esta consulta ira rapido sin importar cuántos miles de tareas existan.
    return await task_service.get_user_tasks(user_id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskUpdate):
    # Actualiza el estado de la tarea (ej: marcarla como completed=True o cambiar el título).
    updated_task = await task_service.update_task(task_id, task)

    # Si la base de datos no encuentra la tarea con ese ID, el servicio
    # devuelve None y lanzamos el error 404 Not Found.
    if not updated_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    return updated_task

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    # Elimina una tarea permanentemente de la colección de MongoDB.
    # Si el servicio devuelve False (no se pudo borrar porque no existe), lanzamos 404.
    if not await task_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Si fue un éxito, devolvemos un JSON de confirmación.
    return {"message": "Tarea eliminada correctamente."}