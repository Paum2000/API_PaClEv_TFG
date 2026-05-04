from fastapi import HTTPException, status
from app.models.schedule import WeekSchedule, BlockWeekSchedule
from app.schemas.schedule import (
    WeekScheduleCreate, WeekScheduleUpdate,
    BlockCreate, BlockUpdate
)


# UTILIDADES DE SEGURIDAD INTERNAS
async def _get_schedule_or_404(schedule_id: int, user_id: int) -> WeekSchedule:
    schedule = await WeekSchedule.get(schedule_id)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado")
    if schedule.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para acceder a este horario")
    return schedule

async def _get_block_and_verify_owner(block_id: int, user_id: int) -> BlockWeekSchedule:
    block = await BlockWeekSchedule.get(block_id)
    if not block:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bloque no encontrado")

    schedule = await WeekSchedule.get(block.week_schedule_id)
    if not schedule or schedule.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre este bloque")

    return block

# LÓGICA DE HORARIOS BASE
async def create_schedule(user_id: int, schedule_in: WeekScheduleCreate) -> WeekSchedule:
    new_schedule = WeekSchedule(**schedule_in.model_dump(), user_id=user_id)
    await new_schedule.insert()
    return new_schedule

async def get_schedules_by_user(user_id: int) -> list[WeekSchedule]:
    return await WeekSchedule.find(WeekSchedule.user_id == user_id).to_list()

async def update_schedule(user_id: int, schedule_id: int, schedule_in: WeekScheduleUpdate) -> WeekSchedule:
    schedule = await _get_schedule_or_404(schedule_id, user_id)

    update_data = schedule_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(schedule, key, value)

    await schedule.save()
    return schedule

async def delete_schedule(user_id: int, schedule_id: int):
    schedule = await _get_schedule_or_404(schedule_id, user_id)
    await BlockWeekSchedule.find(BlockWeekSchedule.week_schedule_id == schedule_id).delete()
    await schedule.delete()

# LÓGICA DE BLOQUES
async def get_blocks_by_schedule(user_id: int, schedule_id: int) -> list[BlockWeekSchedule]:
    await _get_schedule_or_404(schedule_id, user_id)
    return await BlockWeekSchedule.find(BlockWeekSchedule.week_schedule_id == schedule_id).to_list()

async def create_block(user_id: int, schedule_id: int, block_in: BlockCreate) -> BlockWeekSchedule:
    await _get_schedule_or_404(schedule_id, user_id)
    new_block = BlockWeekSchedule(**block_in.model_dump(), week_schedule_id=schedule_id)
    await new_block.insert()
    return new_block

async def update_block(user_id: int, block_id: int, block_in: BlockUpdate) -> BlockWeekSchedule:
    block = await _get_block_and_verify_owner(block_id, user_id)

    update_data = block_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(block, key, value)

    await block.save()
    return block

async def delete_block(user_id: int, block_id: int):
    block = await _get_block_and_verify_owner(block_id, user_id)
    await block.delete()