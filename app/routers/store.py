from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.models.user import User
from app.models.inventory import UserInventory 
from app.services import store_service
from app.core.security import get_current_user

router = APIRouter(prefix="/store", tags=["Store"])

class ColorBuyRequest(BaseModel):
    hex_color: str = Field(..., description="Código hexadecimal del color, ej. #FF5733")

# --- 💡 ESTE ES EL ENDPOINT QUE FALTABA ---
@router.get("/my-inventory")
async def get_my_inventory(current_user: User = Depends(get_current_user)):
    # Llamamos al servicio para obtener la combinación de items
    return await store_service.get_user_inventory(current_user)

@router.post("/buy-theme/{theme_id}")
async def buy_theme(theme_id: int, current_user: User = Depends(get_current_user)):
    result, error_msg = await store_service.buy_theme(current_user, theme_id)
    if error_msg:
        code = status.HTTP_404_NOT_FOUND if "no encontrado" in error_msg else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=error_msg)
    return result

@router.post("/buy-color")
async def buy_color(request: ColorBuyRequest, current_user: User = Depends(get_current_user)):
    result, error_msg = await store_service.buy_color(current_user, request.hex_color)
    if error_msg:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)
    return result