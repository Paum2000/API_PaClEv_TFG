from fastapi import APIRouter
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}

@router.get("/user/{user_id}", response_model=List[TaskOut])
def get_user_tasks(user_id: int):
    return [{"message": "Endpoint listo. Lógica pendiente en ramas."}]

# --- NUEVOS ENDPOINTS ---

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate):
    return {"message": "Endpoint de edición listo. Lógica pendiente."}

@router.delete("/{task_id}")
def delete_task(task_id: int):
    return {"message": f"Tarea {task_id} eliminada. Lógica pendiente."}