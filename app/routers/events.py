from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.models.event import EventCreate, EventOut, EventUpdate
from app.services import event_service
from app.db.session import get_session

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_session)):
    return event_service.create_event(db, event)

@router.get("/user/{user_id}", response_model=List[EventOut])
def get_user_events(user_id: int, db: Session = Depends(get_session)):
    return event_service.get_user_events(db, user_id)

@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_session)):
    updated_event = event_service.update_event(db, event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return updated_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_session)):
    if not event_service.delete_event(db, event_id):
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {"message": "Evento eliminado correctamente."}