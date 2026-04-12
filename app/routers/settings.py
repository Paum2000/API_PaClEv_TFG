from fastapi import APIRouter, HTTPException, Depends
from app.schemas.setting import SettingCreate, SettingOut, SettingUpdate
from app.services import setting_service
from app.core.security import get_current_user
from app.models.user import User

# Todas las rutas de este archivo responderán bajo el prefijo "/settings"
# y se agruparán en Swagger bajo la etiqueta "Settings".
router = APIRouter(prefix="/settings", tags=["Settings"])

@router.post("/", response_model=SettingOut)
async def create_setting(
        setting: SettingCreate,
        current_user: User = Depends(get_current_user)
):
    # Pisamos el user_id que venga en el JSON
    # con el ID real del token. Así es imposible que se la cree a otro.
    setting.user_id = current_user.id
    # Recibe el esquema SettingCreate (que exige user_id y theme_id)
    # y se lo pasa al servicio para guardarlo en MongoDB.
    return await setting_service.create_setting(setting)

# response_model=SettingOut (Sin List): Indica que devolveremos un solo objeto.
@router.get("/my_settings", response_model=SettingOut)
async def get_user_setting(current_user: User = Depends(get_current_user)):
    # Busca la configuración específica de un usuario.
    # Como la relación es 1 a 1, solo habrá un documento por usuario.
    setting = await setting_service.get_user_setting(current_user.id)

    # Si el usuario es nuevo y aún no ha configurado nada (o no se creó
    # automáticamente en el registro), lanzamos un error 404.
    if not setting:
        raise HTTPException(
            status_code=404,
            detail="Configuración no encontrada para este usuario"
        )
    return setting

@router.put("/{setting_id}", response_model=SettingOut)
async def update_setting(
        setting_id: int,
        setting: SettingUpdate,
        current_user: User = Depends(get_current_user)
):
    # 1. Buscamos cuál es la configuración que le pertenece a este usuario
    config_del_usuario = await setting_service.get_user_setting(current_user.id)

    # 2. Comprobamos si no tiene configuración o si está intentando modificar
    # una ID de configuración que no es la suya.
    if not config_del_usuario or config_del_usuario.id != setting_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta configuración")

    # 3. Si es suya, actualizamos
    updated_setting = await setting_service.update_setting(setting_id, setting)
    return updated_setting

@router.delete("/{setting_id}")
async def delete_setting(
        setting_id: int,
        current_user: User = Depends(get_current_user)
):
    # 1. Misma comprobación de identidad
    config_del_usuario = await setting_service.get_user_setting(current_user.id)

    if not config_del_usuario or config_del_usuario.id != setting_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar esta configuración")

    # 2. Borrado seguro
    await setting_service.delete_setting(setting_id)
    return {"message": "Configuración eliminada correctamente."}