from datetime import datetime

from beanie import Document, Indexed, before_event, Insert, Replace, Save
from pydantic import Field, ConfigDict
from typing import Optional
from app.schemas.event import EventBase

class Event(Document, EventBase):
    id: Optional[int] = Field(default=None, alias="_id")

    # Mantenemos el user_id indexado para las búsquedas del GET
    user_id: Indexed(int)


    class Settings:
        name = "events"

    @before_event([Insert, Replace, Save])
    def serialize_dates(self):
        if isinstance(self.start_date, datetime.date):
            self.start_date = self.start_date.isoformat()
        if self.start_time and isinstance(self.start_time, datetime.time):
            self.start_time = self.start_time.isoformat()
        if self.end_date and isinstance(self.end_date, datetime.date):
            self.end_date = self.end_date.isoformat()
        if self.end_time and isinstance(self.end_time, datetime.time):
            self.end_time = self.end_time.isoformat()

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()

