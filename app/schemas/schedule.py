from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# ESQUEMAS PARA EL HORARIO (WeekSchedule)
class WeekScheduleBase(BaseModel):
    title: Optional[str] = None

class WeekScheduleCreate(WeekScheduleBase):
    pass

class WeekScheduleOut(WeekScheduleBase):
    id: int = Field(alias="_id")
    user_id: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class WeekScheduleUpdate(BaseModel):
    title: Optional[str] = None

# ESQUEMAS PARA LOS BLOQUES (BlockWeekSchedule)
class BlockBase(BaseModel):
    title: Optional[str] = None
    weekDay: int
    startHour: str
    endHour: str
    description: Optional[str] = None
    color: Optional[str] = None

class BlockCreate(BlockBase):
    pass

class BlockOut(BlockBase):
    id: int = Field(alias="_id")
    week_schedule_id: int

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class BlockUpdate(BaseModel):
    title: Optional[str] = None
    weekDay: Optional[int] = None
    startHour: Optional[str] = None
    endHour: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None