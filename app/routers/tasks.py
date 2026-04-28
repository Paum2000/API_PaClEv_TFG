from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service
from app.core.security import get_current_user
from app.models.user import User

# Todas las rutas de este archivo tendrán el prefijo "/tasks"
# y se agruparán bajo la etiqueta "Tasks" en la documentación de Swagger.
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# response_model=TaskOut: Nos asegura que el frontend recibirá el 'id' generado.
@router.post("/", response_model=TaskOut)
async def create_task(
        task_in: TaskCreate,
        user_obj: User = Depends(get_current_user)
):
    # Sobrescribimos el user_id para garantizar que la tarea
    # se asigna al usuario dueño del token.
    task_in.user_id = user_obj.id
    # Recibe el esquema TaskCreate (exige title y user_id)
    # y lo envía al servicio para guardarlo en la base de datos.
    return await task_service.create_task(task_in)

# response_model=List[TaskOut]: Crucial aquí. Le indica a FastAPI que
# la respuesta será un arreglo (array) de múltiples tareas.
@router.get("/my_tasks", response_model=List[TaskOut])
async def get_user_tasks(
        user_obj: User = Depends(get_current_user)
):
    # Busca todas las tareas asociadas a un usuario en particular.
    # Como pusimos un índice (Indexed) en user_id en el modelo de base de datos,
    # esta consulta ira rapido sin importar cuántos miles de tareas existan.
    return await task_service.get_user_tasks(user_obj.id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
        task_id: int,
        task: TaskUpdate,
        current_user: User = Depends(get_current_user)
):
    # 1. Buscamos la tarea original en la base de datos
    tarea_original = await task_service.get_task(task_id)

    if not tarea_original:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 2. Comprobamos si el dueño es el que hace la petición
    if tarea_original.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta tarea")

    # 3. Actualizamos la tarea
    updated_task = await task_service.update_task(task_id, task)
    return updated_task

@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        current_user: User = Depends(get_current_user)
):
    # 1. Buscamos la tarea original
    tarea_original = await task_service.get_task(task_id)

    if not tarea_original:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # 2. Comprobamos la identidad para evitar que borren tareas de otros
    if tarea_original.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar esta tarea")

    # 3. Borrado autorizado
    await task_service.delete_task(task_id)
    return {"message": "Tarea eliminada correctamente."}