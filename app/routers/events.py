from fastapi import APIRouter, HTTPException
from typing import List
from app.models.event import EventCreate, EventOut, EventUpdate
from app.services import event_service

# prefix="/events": Todas las rutas aquí empezarán con /events automáticamente.
# tags=["Events"]: Agrupa estos endpoints bajo la sección "Events" en la
# documentación automática de Swagger (http://localhost:8000/docs).
router = APIRouter(prefix="/events", tags=["Events"])

# response_model=EventOut: Le dice a FastAPI que filtre la respuesta usando
# el esquema EventOut (asegurando que devuelva el ID y omita datos sensibles si los hubiera).
@router.post("/", response_model=EventOut)
async def create_event(event: EventCreate):
    # Recibe los datos validados por EventCreate y se los pasa al servicio
    # para que los guarde en la base de datos.
    return await event_service.create_event(event)

# response_model=List[EventOut]: Indica que devolveremos una LISTA de eventos.
@router.get("/user/{user_id}", response_model=List[EventOut])
async def get_user_events(user_id: int):
    # Busca todas las tareas asociadas a un user_id específico.
    # Gracias al índice 'Indexed(int)' que pusimos en el modelo, esta
    # búsqueda será rapidísima en MongoDB.
    return await event_service.get_user_events(user_id)

# Recibe el ID por la URL y los datos a actualizar por el body (EventUpdate).
@router.put("/{event_id}", response_model=EventOut)
async def update_event(event_id: int, event: EventUpdate):
    # Intenta actualizar el evento. Si el servicio devuelve None (porque
    # el ID no existe en la base de datos), lanzamos un error 404 limpio.
    updated_event = await event_service.update_event(event_id, event)

    # Manejo de errores: Si no se encontró el evento, cortamos la ejecución
    # y le avisamos al cliente con un código HTTP 404 (Not Found).
    if not updated_event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    return updated_event

@router.delete("/{event_id}")
async def delete_event(event_id: int):
    # Intenta borrar el evento. Igual que en el PUT, si el servicio indica
    # que no se pudo borrar (ej: no existía), lanzamos un 404.
    if not await event_service.delete_event(event_id):
        raise HTTPException(status_code=404, detail="Evento no encontrado")

    # Si todo sale bien, devolvemos un mensaje de éxito.
    return {"message": "Evento eliminado correctamente."}