from sqlmodel import Session, select
from app.models.event import Event, EventCreate, EventUpdate

def create_event(db: Session, event_in: EventCreate):
    db_event = Event.model_validate(event_in)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_user_events(db: Session, user_id: int):
    statement = select(Event).where(Event.user_id == user_id)
    return db.exec(statement).all()

def update_event(db: Session, event_id: int, event_in: EventUpdate):
    db_event = db.get(Event, event_id)
    if not db_event:
        return None

    update_data = event_in.model_dump(exclude_unset=True)
    db_event.sqlmodel_update(update_data)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.get(Event, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False