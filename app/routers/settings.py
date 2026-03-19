from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.setting import SettingCreate, SettingOut, SettingUpdate
from app.services import setting_service
from app.db.session import get_session

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.post("/", response_model=SettingOut)
def create_setting(setting: SettingCreate, db: Session = Depends(get_session)):
    return setting_service.create_setting(db, setting)

@router.get("/user/{user_id}", response_model=SettingOut)
def get_user_setting(user_id: int, db: Session = Depends(get_session)):
    setting = setting_service.get_user_setting(db, user_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada para este usuario")
    return setting

@router.put("/{setting_id}", response_model=SettingOut)
def update_setting(setting_id: int, setting: SettingUpdate, db: Session = Depends(get_session)):
    updated_setting = setting_service.update_setting(db, setting_id, setting)
    if not updated_setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return updated_setting

@router.delete("/{setting_id}")
def delete_setting(setting_id: int, db: Session = Depends(get_session)):
    if not setting_service.delete_setting(db, setting_id):
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return {"message": "Configuración eliminada correctamente."}