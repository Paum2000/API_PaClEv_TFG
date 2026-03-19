from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: bool = False
    is_recurring: bool = False
    recurrence: Optional[str] = None
    color: Optional[str] = None

class EventCreate(EventBase):
    user_id: int

class EventOut(EventBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    is_recurring: Optional[bool] = None
    recurrence: Optional[str] = None
    color: Optional[str] = None