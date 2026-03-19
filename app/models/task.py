from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    done_date: datetime
    done: bool = False
    color: Optional[str] = None
    priority: str = "Media"
    user_id: int = Field(foreign_key="users.id")

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    owner: Optional["User"] = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: Optional[bool] = None
    color: Optional[str] = None
    priority: Optional[str] = None

class TaskOut(TaskBase):
    id: int