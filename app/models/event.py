from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional
from app.schemas.event import EventBase

class Event(Document, EventBase):
    id: Optional[int] = Field(default=None, alias="_id")

    # Mantenemos el user_id indexado para las búsquedas del GET
    user_id: Indexed(int)

    class Settings:
        name = "events"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()

