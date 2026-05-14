from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.user import User
from app.schemas.social import GroupCreate, GroupUpdate, GroupOut, GroupMemberAdd, GroupMemberOut
from app.services import group_service
from app.core.security import get_current_user
from app.services.group_service import is_user_in_group

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/", response_model=GroupOut)
async def create_new_group(group_data: GroupCreate, current_user: User = Depends(get_current_user)):
    return await group_service.create_group(current_user, group_data.name)

@router.get("/my_groups", response_model=List[GroupOut])
async def get_my_groups(current_user: User = Depends(get_current_user)):
    # Simplemente llamamos al servicio que acabamos de crear
    return await group_service.get_my_groups(current_user.id)

@router.put("/{group_id}", response_model=GroupOut)
async def update_existing_group(group_id: int, group_data: GroupUpdate, current_user: User = Depends(get_current_user)):
    group, error = await group_service.update_group(current_user, group_id, group_data.name)
    if error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error)
    return group

@router.delete("/{group_id}")
async def remove_group(group_id: int, current_user: User = Depends(get_current_user)):
    success, error = await group_service.delete_group(current_user, group_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=error)
    return {"message": "Grupo eliminado correctamente"}

@router.post("/{group_id}/members")
async def add_member(group_id: int, member_data: GroupMemberAdd, current_user: User = Depends(get_current_user)):
    success, error = await group_service.add_member_to_group(current_user, group_id, member_data.user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"message": "Miembro añadido al grupo"}

@router.get("/{group_id}/members", response_model=List[GroupMemberOut])
async def get_members(group_id: int, current_user: User = Depends(get_current_user)):

    # 1. Ejecutamos tu función y guardamos el resultado (True o False)
    pertenece = await is_user_in_group(current_user.id, group_id)

    # 2. Si devuelve False, cerramos la puerta de golpe
    if not pertenece:
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: No perteneces a este grupo"
        )

    # 3. Si llega hasta aquí, es que es True. Le damos los datos.
    return await group_service.get_group_members(group_id)

@router.delete("/{group_id}/members/{user_id}")
async def remove_member(group_id: int, user_id: int, current_user: User = Depends(get_current_user)):
    """
    Elimina a un miembro del grupo.
    Sirve para que el admin expulse a alguien o para que un usuario abandone el grupo.
    """
    success, error = await group_service.remove_member_from_group(current_user, group_id, user_id)
    if not success:
        # Usamos 403 si es un problema de permisos o 400 si es lógica de negocio
        status_code = status.HTTP_403_FORBIDDEN if "permisos" in error else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=error)

    return {"message": "Miembro eliminado del grupo correctamente"}

@router.get("/{group_id}", response_model=GroupOut)
async def get_group_details(group_id: int, current_user: User = Depends(get_current_user)):

    # 1. Comprobamos con la misma función si el usuario está dentro
    pertenece = await is_user_in_group(current_user.id, group_id)

    # 2. Si es un intruso, lanzamos el 403
    if not pertenece:
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado: No puedes ver los detalles de un grupo al que no perteneces"
        )

    # 3. Si llega hasta aquí, llamamos a la función limpia del service
    return await group_service.get_group(group_id)

