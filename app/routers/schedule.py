from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.schedule import WeekScheduleCreate, WeekScheduleOut, WeekScheduleUpdate,BlockCreate, BlockOut, BlockUpdate
from app.services import schedule_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/schedules", tags=["Schedules"])

# ENDPOINTS DE LOS HORARIOS BASE
@router.post("/", response_model=WeekScheduleOut)
async def create_schedule(
        schedule_in: WeekScheduleCreate,
        current_user: User = Depends(get_current_user)
):
    return await schedule_service.create_schedule(current_user.id, schedule_in)

@router.get("/", response_model=List[WeekScheduleOut])
async def get_my_schedules(current_user: User = Depends(get_current_user)):
    return await schedule_service.get_schedules_by_user(current_user.id)

@router.put("/{schedule_id}", response_model=WeekScheduleOut)
async def update_schedule(
        schedule_id: int,
        schedule_in: WeekScheduleUpdate,
        current_user: User = Depends(get_current_user)
):
    return await schedule_service.update_schedule(current_user.id, schedule_id, schedule_in)

@router.delete("/{schedule_id}")
async def delete_schedule(
        schedule_id: int,
        current_user: User = Depends(get_current_user)
):
    await schedule_service.delete_schedule(current_user.id, schedule_id)
    return {"message": "Horario y sus bloques eliminados correctamente"}


# ENDPOINTS DE LOS BLOQUES (Por ID de Horario)
@router.get("/{schedule_id}/blocks", response_model=List[BlockOut])
async def get_blocks(
        schedule_id: int,
        current_user: User = Depends(get_current_user)
):
    return await schedule_service.get_blocks_by_schedule(current_user.id, schedule_id)

@router.post("/{schedule_id}/blocks", response_model=BlockOut)
async def create_block(
        schedule_id: int,
        block_in: BlockCreate,
        current_user: User = Depends(get_current_user)
):
    return await schedule_service.create_block(current_user.id, schedule_id, block_in)

@router.put("/blocks/{block_id}", response_model=BlockOut)
async def update_block(
        block_id: int,
        block_in: BlockUpdate,
        current_user: User = Depends(get_current_user)
):
    return await schedule_service.update_block(current_user.id, block_id, block_in)

@router.delete("/blocks/{block_id}")
async def delete_block(
        block_id: int,
        current_user: User = Depends(get_current_user)
):
    await schedule_service.delete_block(current_user.id, block_id)
    return {"message": "Bloque eliminado correctamente"}