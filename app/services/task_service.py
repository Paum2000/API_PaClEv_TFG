from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

# 1. CREATE
async def create_task(task_in: TaskCreate):
    new_task = Task(**task_in.model_dump())
    await new_task.insert()
    return new_task

# 2. GET USER TASKS
async def get_user_tasks(user_id: int):
    tasks = await Task.find(Task.user_id == user_id).to_list()
    return tasks

# 3. GET SINGLE TASK
async def get_task(task_id: int):
    task = await Task.get(task_id)
    return task

# 4. UPDATE
async def update_task(task_id: int, task_in: TaskUpdate):
    task = await Task.get(task_id)
    if task:
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        await task.save()
    return task

# 5. DELETE
async def delete_task(task_id: int):
    task = await Task.get(task_id)
    if task:
        await task.delete()