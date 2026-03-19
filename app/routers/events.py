from fastapi import APIRouter
from typing import List
from app.schemas.event import EventCreate, EventOut, EventUpdate

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventOut)
def create_event(event: EventCreate):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}

@router.get("/user/{user_id}", response_model=List[EventOut])
def get_user_events(user_id: int):
    return [{"message": "Endpoint listo. Lógica pendiente en ramas."}]

@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, event: EventUpdate):
    return {"message": "Endpoint de edición listo. Lógica pendiente."}

@router.delete("/{event_id}")
def delete_event(event_id: int):
    return {"message": f"Evento {event_id} eliminado. Lógica pendiente."}