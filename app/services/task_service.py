from sqlmodel import Session, select
from app.models.task import Task, TaskCreate, TaskUpdate

# --- 1. CREAR TAREA (CREATE) ---
def create_task(db: Session, task_in: TaskCreate):
    # 'model_validate' toma los datos validados del esquema TaskCreate
    # y los convierte en una instancia del modelo de base de datos Task.
    db_task = Task.model_validate(task_in)

    db.add(db_task)      # Preparamos la inserción
    db.commit()          # Guardamos en la tabla 'tasks'
    db.refresh(db_task)  # Recuperamos el ID y otros valores generados por la DB
    return db_task

# --- 2. LEER TAREAS DE UN USUARIO (READ) ---
def get_user_tasks(db: Session, user_id: int):
    # Aquí no traemos todas las tareas del sistema,
    # sino que filtramos usando '.where' para que el usuario solo vea sus tareas.
    # Es el equivalente a: SELECT * FROM tasks WHERE user_id = :user_id;
    statement = select(Task).where(Task.user_id == user_id)

    # Ejecutamos la consulta y devolvemos la lista de tareas.
    return db.exec(statement).all()

# --- 3. ACTUALIZAR TAREA (UPDATE) ---
def update_task(db: Session, task_id: int, task_in: TaskUpdate):
    # Buscamos la tarea específica por su ID.
    db_task = db.get(Task, task_id)
    if not db_task:
        return None # Si la tarea no existe (o fue borrada), no hacemos nada.

    # Convertimos el modelo de actualización a un diccionario.
    # 'exclude_unset=True' es vital: permite marcar una tarea como 'done'
    # sin tener que enviar el título o la descripción de nuevo.
    update_data = task_in.model_dump(exclude_unset=True)

    # Aplicamos los cambios al objeto que ya tenemos en memoria.
    db_task.sqlmodel_update(update_data)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# --- 4. BORRAR TAREA (DELETE) ---
def delete_task(db: Session, task_id: int):
    # Localizamos la tarea.
    db_task = db.get(Task, task_id)
    if db_task:
        db.delete(db_task) # Solicitamos el borrado
        db.commit()        # Ejecutamos la transacción
        return True
    return False # Retornamos False si el ID no correspondía a ninguna tarea.