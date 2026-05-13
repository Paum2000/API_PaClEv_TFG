from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.user import User
from app.schemas.social import FriendRequest, FriendOut, FriendDetailOut
from app.services import social_service
from app.core.security import get_current_user

router = APIRouter(prefix="/friends", tags=["Social"])

@router.post("/request", response_model=FriendOut)
async def send_request(request_data: FriendRequest, current_user: User = Depends(get_current_user)):
    request, error = await social_service.send_friend_request(current_user, request_data.friend_id)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return request

@router.post("/accept/{request_id}")
async def accept_request(request_id: int, current_user: User = Depends(get_current_user)):
    success, error = await social_service.accept_friend_request(current_user, request_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return {"message": "Solicitud de amistad aceptada"}

@router.get("/my_friends",response_model=List[FriendDetailOut])
async def list_my_friends(current_user: User = Depends(get_current_user)):
    return await social_service.get_my_friends(current_user.id)

@router.delete("/{friend_id}")
async def delete_friend(friend_id: int, current_user: User = Depends(get_current_user)):
    success, error = await social_service.remove_friendship(current_user, friend_id)

    if not success:
        # Si no existe la relación, lanzamos un 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)

    return {"message": "Relación de amistad eliminada correctamente"}