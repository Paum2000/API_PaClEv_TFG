from sqlmodel import Session, select
from app.models.setting import Setting, SettingCreate, SettingUpdate

# --- 1. CREAR CONFIGURACIÓN (CREATE) ---
def create_setting(db: Session, setting_in: SettingCreate):
    # Usamos 'model_validate' para validar los datos que envía el usuario
    # (idioma, color, tema) directamente al objeto de la base de datos.
    db_setting = Setting.model_validate(setting_in)

    db.add(db_setting)      # Añadimos el registro a la sesión actual
    db.commit()          # Guardamos los cambios en la tabla 'settings'
    db.refresh(db_setting)  # Obtenemos el ID y los valores finales
    return db_setting

# --- 2. OBTENER CONFIGURACIÓN DEL USUARIO (READ) ---
def get_user_setting(db: Session, user_id: int):
    # Aquí usamos '.first()' en lugar de '.all()'.
    # Como cada usuario solo debe tener una configuración, buscamos
    # el primer registro que coincida con su 'user_id'.
    statement = select(Setting).where(Setting.user_id == user_id)

    # Si el usuario no tiene configuración, esto devolverá 'None'.
    return db.exec(statement).first()

# --- 3. ACTUALIZAR CONFIGURACIÓN (UPDATE) ---
def update_setting(db: Session, setting_id: int, setting_in: SettingUpdate):
    # Buscamos la configuración existente por su ID único.
    db_setting = db.get(Setting, setting_id)
    if not db_setting:
        return None

    # 'exclude_unset=True' permite que si el usuario solo quiere cambiar
    # el idioma, no se borre el color de acento o el tema actual.
    update_data = setting_in.model_dump(exclude_unset=True)

    # Aplicamos los cambios detectados al objeto de la base de datos.
    db_setting.sqlmodel_update(update_data)

    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting

# --- 4. BORRAR CONFIGURACIÓN (DELETE) ---
def delete_setting(db: Session, setting_id: int):
    db_setting = db.get(Setting, setting_id)
    if db_setting:
        db.delete(db_setting) # Preparamos la eliminación
        db.commit()           # Confirmamos el borrado
        return True
    return False # Retornamos False si el registro no existía