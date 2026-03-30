from beanie import Document, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional
# Importamos la base desde tus esquemas
from app.schemas.theme import ThemeBase

class Theme(Document, ThemeBase):
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        name = "themes"

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()