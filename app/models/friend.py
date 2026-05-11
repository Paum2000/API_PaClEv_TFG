from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional

class Friend(Document):
    id: Optional[int] = Field(default=None, alias="_id")
    user_id_1: Indexed(int)
    user_id_2: Indexed(int)
    status: str = "PENDIENTE"

    class Settings:
        name = "friends"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()