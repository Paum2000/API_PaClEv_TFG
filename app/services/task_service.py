from sqlmodel import Session, select
from app.models.task import Task, TaskCreate, TaskUpdate

def create_task(db: Session, task_in: TaskCreate):
    db_task = Task.model_validate(task_in)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_user_tasks(db: Session, user_id: int):
    statement = select(Task).where(Task.user_id == user_id)
    return db.exec(statement).all()

def update_task(db: Session, task_id: int, task_in: TaskUpdate):
    db_task = db.get(Task, task_id)
    if not db_task:
        return None

    update_data = task_in.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(update_data)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.get(Task, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False