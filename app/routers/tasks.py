from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.models.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service
from app.db.session import get_session

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_session)):
    return task_service.create_task(db, task)

@router.get("/user/{user_id}", response_model=List[TaskOut])
def get_user_tasks(user_id: int, db: Session = Depends(get_session)):
    return task_service.get_user_tasks(db, user_id)

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_session)):
    updated_task = task_service.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_session)):
    if not task_service.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada correctamente."}