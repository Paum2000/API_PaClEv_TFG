from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
async def create_task(
        task: TaskCreate,
        current_user: User = Depends(get_current_user) 
):
    task.user_id = current_user.id
    return await task_service.create_task(task)

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