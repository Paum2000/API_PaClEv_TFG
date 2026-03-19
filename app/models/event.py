from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class EventBase(SQLModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: bool = False
    is_recurring: bool = False
    recurrence: Optional[str] = None
    color: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")

class Event(EventBase, table=True):
    __tablename__ = "events"
    id: Optional[int] = Field(default=None, primary_key=True)
    owner: Optional["User"] = Relationship(back_populates="events")

class EventCreate(EventBase):
    pass

class EventUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    is_recurring: Optional[bool] = None
    recurrence: Optional[str] = None
    color: Optional[str] = None

class EventOut(EventBase):
    id: int