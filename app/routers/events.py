from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.event import EventCreate, EventOut, EventUpdate, EventBase
from app.services import event_service
from app.core.security import get_current_user
from app.models.user import User

# prefix="/events": Todas las rutas aquí empezarán con /events automáticamente.
# tags=["Events"]: Agrupa estos endpoints bajo la sección "Events" en la
# documentación automática de Swagger (http://localhost:8000/docs).
router = APIRouter(prefix="/events", tags=["Events"])

# response_model=EventOut: Le dice a FastAPI que filtre la respuesta usando
# el esquema EventOut (asegurando que devuelva el ID y omita datos sensibles si los hubiera).
@router.post("/", response_model=EventOut)
async def create_event(
        event_in: EventBase,
        current_user: User = Depends(get_current_user)
):
    # Convertimos los datos que envía el usuario a un diccionario
    event_data = event_in.model_dump()

    # Le inyectamos automáticamente el ID del dueño del token
    event_data["user_id"] = current_user.id

    # Creamos el esquema EventCreate que espera el servicio
    event_to_create = EventCreate(**event_data)

    return await event_service.create_event(event_to_create)

# response_model=List[EventOut]: Indica que devolveremos una LISTA de eventos.
@router.get("/my_events", response_model=List[EventOut])
async def get_user_events(
        current_user: User = Depends(get_current_user)
):
    # Buscamos los eventos usando directamente el ID del token
    return await event_service.get_user_events(current_user.id)

# Recibe el ID por la URL y los datos a actualizar por el body (EventUpdate).
@router.put("/{event_id}", response_model=EventOut)
async def update_event(
        event_id: int,
        event: EventUpdate,
        current_user: User = Depends(get_current_user)
):
    # 1. Buscamos el evento ORIGINAL en la base de datos
    original_event = await event_service.get_event(event_id)

    # Si no existe, no seguimos
    if not original_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # 2. Comprobamos si el dueño real en la BD es el que hace la petición
    if original_event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este evento")

    # 3. Si es suyo, entonces SÍ llamamos a tu método para que lo actualice
    updated_event = await event_service.update_event(event_id, event)

    return updated_event

@router.delete("/{event_id}")
async def delete_event(
        event_id: int,
        current_user: User = Depends(get_current_user)
):
    # 1. Buscamos el evento primero
    event = await event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # 2. Comprobamos si el dueño es el que está haciendo la petición
    if event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar este evento")

    # 3. Si llegamos aquí, es seguro borrarlo
    await event_service.delete_event(event_id)
    return {"message": "Evento eliminado correctamente."}