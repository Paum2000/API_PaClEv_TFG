from fastapi import APIRouter, HTTPException
from typing import List

from app.models.event import EventCreate, EventOut, EventUpdate
from app.services import event_service

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventOut)
async def create_event(event: EventCreate):
    return await event_service.create_event(event)

@router.get("/user/{user_id}", response_model=List[EventOut])
async def get_user_events(user_id: int):
    return await event_service.get_user_events(user_id)

@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: int, event: EventUpdate):
    updated_event = await event_service.update_event(event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return updated_event

@router.delete("/{event_id}")
async def delete_event(event_id: int):
    if not await event_service.delete_event(event_id):
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {"message": "Evento eliminado correctamente."}