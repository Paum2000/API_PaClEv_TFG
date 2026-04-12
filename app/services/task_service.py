from app.models.task import Task
from typing import List, Optional
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    await task.insert()
    return task

async def get_task(task_id: int) -> Optional[Task]:
    # Busca y devuelve una única tarea por su ID
    return await Task.get(task_id)

async def get_user_tasks(user_id: int) -> List[Task]:
    # Busca todas las tareas que pertenezcan a este usuario y las devuelve en una lista
    return await Task.find(Task.user_id == user_id).to_list()

async def update_task(task_id: int, task_in: TaskUpdate) -> Optional[Task]:
    task = await Task.get(task_id)
    if not task:
        return None

    update_data = task_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    await task.save()
    return task

async def delete_task(task_id: int) -> bool:
    task = await Task.get(task_id)
    if task:
        await task.delete()
        return True
    return False