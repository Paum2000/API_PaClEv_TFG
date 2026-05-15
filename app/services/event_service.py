from beanie.odm.operators.find.comparison import In
from beanie.odm.operators.find.logical import Or

from app.models.event import Event
from typing import List, Optional

from app.models.group_member import GroupMember
from app.schemas.event import EventCreate, EventUpdate


async def create_event(event_in: EventCreate) -> Event:
    event = Event(**event_in.model_dump())
    await event.insert()
    return event

async def get_user_events(user_id: int) -> List[Event]:
    membresias = await GroupMember.find(GroupMember.user_id == user_id).to_list()
    group_ids = [m.group_id for m in membresias]
    if not group_ids:
        return await Event.find(Event.user_id == user_id).to_list()
    return await Event.find(Or(Event.user_id == user_id, In(Event.group_id, group_ids))).to_list()

async def get_event(event_id: int) -> Optional[Event]:
    # Busca y devuelve un único evento por su ID
    return await Event.get(event_id)

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

async def get_events_by_group(group_id: int):
    #Busca todos los eventos que pertenezcan a un grupo en concreto.
    return  await Event.find(Event.group_id == group_id).to_list()