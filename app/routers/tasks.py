from fastapi import APIRouter, HTTPException
from typing import List

from app.models.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate):
    return await task_service.create_task(task)

@router.get("/user/{user_id}", response_model=List[TaskOut])
async def get_user_tasks(user_id: int):
    return await task_service.get_user_tasks(user_id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskUpdate):
    updated_task = await task_service.update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated_task

@router.delete("/{task_id}")
async def delete_task(task_id: int):
    if not await task_service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada correctamente."}