from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service
from app.core.security import get_current_user, verify_group_access
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
async def create_task(
        task_in: TaskCreate, # Lo llamamos task_in para que sea más claro
        current_user: User = Depends(get_current_user)
):
    # 1. Asignamos el dueño de la tarea
    task_in.user_id = current_user.id

    if task_in.group_id is not None:
        await verify_group_access(task_in.group_id, current_user)

    # 4. Llamamos al servicio
    return await task_service.create_task(task_in)

@router.get("/my_tasks", response_model=List[TaskOut])
async def get_user_tasks(
        current_user: User = Depends(get_current_user)
):
    return await task_service.get_user_tasks(current_user.id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
        task_id: int,
        task: TaskUpdate,
        current_user: User = Depends(get_current_user)
):
    tarea_original = await task_service.get_task(task_id)

    if not tarea_original:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea_original.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta tarea")

    updated_task = await task_service.update_task(task_id, task, current_user)
    return updated_task

@router.delete("/{task_id}")
async def delete_task(
        task_id: int,
        current_user: User = Depends(get_current_user)
):
    tarea_original = await task_service.get_task(task_id)

    if not tarea_original:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    if tarea_original.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar esta tarea")

    await task_service.delete_task(task_id)
    return {"message": "Tarea eliminada correctamente."}

@router.get("/group/{group_id}", response_model=List[TaskOut])
async def get_group_tasks(group_id: int = Depends(verify_group_access)):
    # Obtiene todas las tareas compartidas en un grupo.
    return await task_service.get_tasks_by_group(group_id)