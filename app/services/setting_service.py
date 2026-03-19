from sqlmodel import Session, select
from app.models.setting import Setting, SettingCreate, SettingUpdate

def create_setting(db: Session, setting_in: SettingCreate):
    db_setting = Setting.model_validate(setting_in)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

def get_user_setting(db: Session, user_id: int):
    # Buscamos la configuración específica de un usuario
    statement = select(Setting).where(Setting.user_id == user_id)
    return db.exec(statement).first()

def update_setting(db: Session, setting_id: int, setting_in: SettingUpdate):
    db_setting = db.get(Setting, setting_id)
    if not db_setting:
        return None

    update_data = setting_in.model_dump(exclude_unset=True)
    db_setting.sqlmodel_update(update_data)

    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

def delete_setting(db: Session, setting_id: int):
    db_setting = db.get(Setting, setting_id)
    if db_setting:
        db.delete(db_setting)
        db.commit()
        return True
    return False