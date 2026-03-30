from app.models.setting import Setting
from typing import Optional
from app.schemas.setting import SettingCreate, SettingUpdate


async def create_setting(setting_in: SettingCreate) -> Setting:
    setting = Setting(**setting_in.model_dump())
    await setting.insert()
    return setting

async def get_user_setting(user_id: int) -> Optional[Setting]:
    # find_one() devuelve un único documento que coincida con la condición
    return await Setting.find_one(Setting.user_id == user_id)

async def update_setting(setting_id: int, setting_in: SettingUpdate) -> Optional[Setting]:
    setting = await Setting.get(setting_id)
    if not setting:
        return None

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