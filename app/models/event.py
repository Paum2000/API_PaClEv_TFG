from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.counter import get_next_id_fast

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: datetime
    user_id: Indexed(int)

class Event(Document, EventBase):
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        name = "events"

    @before_event(Insert)
    def assign_id(self):
        if self.id is None:
            self.id = get_next_id_fast()

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None

class EventOut(EventBase):
    id: int
    model_config = ConfigDict(from_attributes=True)