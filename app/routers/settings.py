from fastapi import APIRouter
from app.schemas.setting import SettingCreate, SettingOut, SettingUpdate

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.post("/", response_model=SettingOut)
def create_setting(setting: SettingCreate):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}

# Nota: Settings suele ser 1 a 1 con el usuario, por eso buscamos por user_id
@router.get("/user/{user_id}", response_model=SettingOut)
def get_user_setting(user_id: int):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}

@router.put("/{setting_id}", response_model=SettingOut)
def update_setting(setting_id: int, setting: SettingUpdate):
    return {"message": "Endpoint de edición listo. Lógica pendiente."}

@router.delete("/{setting_id}")
def delete_setting(setting_id: int):
    return {"message": f"Configuración {setting_id} eliminada. Lógica pendiente."}