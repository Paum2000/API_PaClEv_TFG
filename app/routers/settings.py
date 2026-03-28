from fastapi import APIRouter, HTTPException

from app.models.setting import SettingCreate, SettingOut, SettingUpdate
from app.services import setting_service

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.post("/", response_model=SettingOut)
async def create_setting(setting: SettingCreate):
    return await setting_service.create_setting(setting)

@router.get("/user/{user_id}", response_model=SettingOut)
async def get_user_setting(user_id: int):
    setting = await setting_service.get_user_setting(user_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada para este usuario")
    return setting

@router.put("/{setting_id}", response_model=SettingOut)
async def update_setting(setting_id: int, setting: SettingUpdate):
    updated_setting = await setting_service.update_setting(setting_id, setting)
    if not updated_setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return updated_setting

@router.delete("/{setting_id}")
async def delete_setting(setting_id: int):
    if not await setting_service.delete_setting(setting_id):
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return {"message": "Configuración eliminada correctamente."}