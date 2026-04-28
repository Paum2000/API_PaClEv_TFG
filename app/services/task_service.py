from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
async def create_task(task_in: TaskCreate, current_user: User = Depends(get_current_user)):
    task_in.user_id = current_user.id
    return await task_service.create_task(task_in)

@router.get("/my_tasks", response_model=List[TaskOut])
async def get_my_tasks(current_user: User = Depends(get_current_user)):
    # ¡AQUÍ ESTABA EL ERROR! Asegúrate de llamar a get_user_tasks
    return await task_service.get_user_tasks(current_user.id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task_in: TaskUpdate, current_user: User = Depends(get_current_user)):
    task = await task_service.get_task(task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return await task_service.update_task(task_id, task_in)

@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    task = await task_service.get_task(task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    await task_service.delete_task(task_id)
    return {"message": "Tarea eliminada"}