from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.user import User
from datetime import datetime

# --- Lógica de Gamificación ---
async def update_task_points(user: User, is_completing: bool):
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Reset del límite diario si es un nuevo día
    if user.last_points_reset != today:
        user.points_earned_today = 0
        user.last_points_reset = today

    if is_completing:
        # 2. Sumamos si no ha llegado al límite de 100
        if user.points_earned_today < 100:
            puntos_a_sumar = 10
            # Si se va a pasar de 100, ajustamos
            if user.points_earned_today + 10 > 100:
                puntos_a_sumar = 100 - user.points_earned_today

            user.points += puntos_a_sumar
            user.points_earned_today += puntos_a_sumar
    else:
        # 3. Restamos si desmarca la tarea
        if user.points >= 10:
            user.points -= 10
            if user.points_earned_today >= 10:
                user.points_earned_today -= 10

    await user.save()

# --- Funciones CRUD ---

async def create_task(task_in: TaskCreate):
    new_task = Task(**task_in.model_dump())
    await new_task.insert()
    return new_task

async def get_user_tasks(user_id: int):
    return await Task.find(Task.user_id == user_id).to_list()

async def get_task(task_id: int):
    return await Task.get(task_id)

async def update_task(task_id: int, task_in: TaskUpdate, current_user: User):
    task = await Task.get(task_id)
    if task:
        # Guardamos el estado ANTES de modificar
        was_completed = task.completed

        # Aplicamos los cambios que vienen del frontend
        update_data = task_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        await task.save()

        # Comprobamos si el estado de 'completed' ha cambiado
        if "completed" in update_data:
            is_completed_now = task.completed

            # Pasó de falso a verdadero -> ganamos puntos
            if not was_completed and is_completed_now:
                await update_task_points(current_user, is_completing=True)

            # Pasó de verdadero a falso -> perdemos puntos
            elif was_completed and not is_completed_now:
                await update_task_points(current_user, is_completing=False)

    return task

async def delete_task(task_id: int):
    task = await Task.get(task_id)
    if task:
        await task.delete()