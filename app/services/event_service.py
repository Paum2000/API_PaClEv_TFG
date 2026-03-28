from app.models.event import Event, EventCreate, EventUpdate
from typing import List, Optional

async def create_event(event_in: EventCreate) -> Event:
    event = Event(**event_in.model_dump())
    await event.insert()
    return event

async def get_user_events(user_id: int) -> List[Event]:
    # Trae todos los eventos que coincidan con el ID del usuario
    return await Event.find(Event.user_id == user_id).to_list()

async def update_event(event_id: int, event_in: EventUpdate) -> Optional[Event]:
    event = await Event.get(event_id)
    if not event:
        return None

    update_data = event_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(event, key, value)

    await event.save()
    return event

async def delete_event(event_id: int) -> bool:
    event = await Event.get(event_id)
    if event:
        await event.delete()
        return True
    return False