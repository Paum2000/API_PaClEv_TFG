from fastapi import APIRouter, HTTPException
from app.models.setting import SettingCreate, SettingOut, SettingUpdate
from app.services import setting_service

# Todas las rutas de este archivo responderán bajo el prefijo "/settings"
# y se agruparán en Swagger bajo la etiqueta "Settings".
router = APIRouter(prefix="/settings", tags=["Settings"])

@router.post("/", response_model=SettingOut)
async def create_setting(setting: SettingCreate):
    # Recibe el esquema SettingCreate (que exige user_id y theme_id)
    # y se lo pasa al servicio para guardarlo en MongoDB.
    return await setting_service.create_setting(setting)

# response_model=SettingOut (Sin List): Indica que devolveremos un solo objeto.
@router.get("/user/{user_id}", response_model=SettingOut)
async def get_user_setting(user_id: int):
    # Busca la configuración específica de un usuario.
    # Como la relación es 1 a 1, solo habrá un documento por usuario.
    setting = await setting_service.get_user_setting(user_id)

    # Si el usuario es nuevo y aún no ha configurado nada (o no se creó
    # automáticamente en el registro), lanzamos un error 404.
    if not setting:
        raise HTTPException(
            status_code=404,
            detail="Configuración no encontrada para este usuario"
        )
    return setting

@router.put("/{setting_id}", response_model=SettingOut)
async def update_setting(setting_id: int, setting: SettingUpdate):
    # Actualiza campos parciales (theme_id, accent_color, lenguaje).
    updated_setting = await setting_service.update_setting(setting_id, setting)

    if not updated_setting:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")

    return updated_setting

@router.delete("/{setting_id}")
async def delete_setting(setting_id: int):
    # Elimina el documento de configuración de la base de datos.
    if not await setting_service.delete_setting(setting_id):
        raise HTTPException(status_code=404, detail="Configuración no encontrada")

    return {"message": "Configuración eliminada correctamente."}