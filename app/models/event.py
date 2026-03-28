from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.models.counter import get_next_id

class Event(Document):
    id: Optional[int] = Field(default=None)
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: bool = False
    user_id: int # Relación con el usuario

    class Settings:
        name = "events"

    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            self.id = await get_next_id("events_id")

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: Optional[bool] = False
    user_id: int

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    is_all_day: Optional[bool] = None

class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    is_all_day: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)