from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    done_date: datetime
    done: bool = False
    color: Optional[str] = None
    priority: str = "Media"

class TaskCreate(TaskBase):
    user_id: int

class TaskOut(TaskBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True


class TaskUpdate:
    class TaskUpdate(BaseModel):
        title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    done_date: Optional[datetime] = None
    done: Optional[bool] = None
    color: Optional[str] = None
    priority: Optional[str] = None