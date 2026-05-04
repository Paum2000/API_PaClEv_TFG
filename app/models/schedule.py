from beanie import Document, Indexed, before_event, Insert
from pydantic import Field, ConfigDict
from typing import Optional

# --- COLECCIÓN 1: El Horario Base ---
class WeekSchedule(Document):
    id: Optional[int] = Field(default=None, alias="_id")
    user_id: Indexed(int) # FK: Dueño del horario
    title: Optional[str] = None

    class Settings:
        name = "week_schedules" # Primera tabla/colección

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()


# --- COLECCIÓN 2: Los Bloques del Horario ---
class BlockWeekSchedule(Document):
    id: Optional[int] = Field(default=None, alias="_id")

    # FK: A qué horario pertenece este bloque (Índice para búsquedas ultra-rápidas)
    week_schedule_id: Indexed(int)

    title: Optional[str] = None
    weekDay: int
    startHour: str
    endHour: str
    description: Optional[str] = None
    color: Optional[str] = None

    class Settings:
        name = "block_week_schedules" # Segunda tabla/colección

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @before_event(Insert)
    def assign_id(self):
        from app.models.counter import get_next_id_fast
        if self.id is None:
            self.id = get_next_id_fast()