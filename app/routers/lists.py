from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.list import ListCreate, ListOut, ListUpdate
from app.services import list_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/lists", tags=["Lists"])

@router.post("/", response_model=ListOut)
async def create_list(
        list_in: ListCreate,
        current_user: User = Depends(get_current_user)
):
    # Le pasamos el ID del usuario al servicio para asegurar la propiedad
    return await list_service.create_list(list_in, current_user.id)

@router.get("/my_lists", response_model=List[ListOut])
async def get_my_lists(current_user: User = Depends(get_current_user)):
    return await list_service.get_user_lists(current_user.id)

@router.put("/{list_id}", response_model=ListOut)
async def update_list(
        list_id: str,
        list_in: ListUpdate,
        current_user: User = Depends(get_current_user)
):
    # 1. Buscamos la lista
    lista_original = await list_service.get_list(list_id)
    if not lista_original:
        raise HTTPException(status_code=404, detail="Lista no encontrada")

    # 2. Verificamos que sea suya
    if str(lista_original.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permiso para editar esta lista")

    # 3. Actualizamos
    return await list_service.update_list(list_id, list_in)

@router.delete("/{list_id}")
async def delete_list(
        list_id: str,
        current_user: User = Depends(get_current_user)
):
    lista_original = await list_service.get_list(list_id)
    if not lista_original:
        raise HTTPException(status_code=404, detail="Lista no encontrada")

    if str(lista_original.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar esta lista")

    await list_service.delete_list(list_id)
    return {"message": "Lista eliminada correctamente"}