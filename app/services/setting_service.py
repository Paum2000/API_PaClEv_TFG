from app.models.setting import Setting
from app.models.theme import Theme
from app.models.inventory import UserInventory
from typing import Optional
from app.schemas.setting import SettingCreate, SettingUpdate

# --- HELPER DE SEGURIDAD ---
async def _verificar_propiedad_items(user_id: int, theme_id: Optional[int] = None, accent_color: Optional[str] = None):
    # 1. Comprobamos el Tema (si lo está intentando cambiar/crear)
    if theme_id is not None:
        theme_to_apply = await Theme.get(theme_id)
        if not theme_to_apply:
            raise ValueError("El tema seleccionado no existe")

        if not theme_to_apply.is_default:
            has_theme = await UserInventory.find_one(
                UserInventory.user_id == user_id,
                UserInventory.item_type == "THEME",
                UserInventory.item_reference == str(theme_id)
            )
            if not has_theme:
                raise ValueError("No puedes equipar un tema que no has desbloqueado")

    # 2. Comprobamos el Color (si lo está intentando cambiar/crear y no es None)
    if accent_color is not None:
        color_code = accent_color.upper()
        has_color = await UserInventory.find_one(
            UserInventory.user_id == user_id,
            UserInventory.item_type == "COLOR",
            UserInventory.item_reference == color_code
        )
        if not has_color:
            raise ValueError(f"No puedes equipar el color {color_code} porque no lo tienes en tu inventario")


# --- OPERACIONES CRUD ---

async def create_setting(setting_in: SettingCreate, user_id: int) -> Setting:
    # seguridad antes de crear
    await _verificar_propiedad_items(
        user_id=user_id,
        theme_id=setting_in.theme_id,
        accent_color=getattr(setting_in, 'accent_color', None)
    )

    setting = Setting(**setting_in.model_dump(), user_id=user_id)
    await setting.insert()
    return setting

async def get_user_setting(user_id: int) -> Optional[Setting]:
    # find_one() devuelve un único documento que coincida con la condición
    return await Setting.find_one(Setting.user_id == user_id)

async def update_setting(setting_id: int, setting_in: SettingUpdate) -> Optional[Setting]:
    setting = await Setting.get(setting_id)
    if not setting:
        return None

    # seguridad antes de actualizar
    await _verificar_propiedad_items(
        user_id=setting.user_id,
        theme_id=setting_in.theme_id,
        accent_color=setting_in.accent_color
    )

    update_data = setting_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(setting, key, value)

    await setting.save()
    return setting

async def delete_setting(setting_id: int) -> bool:
    setting = await Setting.get(setting_id)
    if setting:
        await setting.delete()
        return True
    return False