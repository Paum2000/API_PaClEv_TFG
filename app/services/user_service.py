from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserUpdate

# --- 1. CREAR (CREATE) ---
def create_user(db: Session, user_in: UserCreate):
    # Convertimos el objeto 'UserCreate' (que viene de la API) en un objeto 'User' (para la DB).
    # Aquí es donde se aplicaria la seguridad.
    db_user = User(
        user_name=user_in.user_name,
        email=user_in.email,
        birthday=user_in.birthday,
        user_photo=user_in.user_photo,
        # La contraseña real nunca se guarda; se guarda una versión cifrada.
        password_hash=user_in.password + "hashed" # Simulación
    )
    db.add(db_user)      # Le decimos a la sesión: "Prepara este usuario para guardarlo"
    db.commit()          # Guardamos físicamente en la base de datos
    db.refresh(db_user)  # Refrescamos para obtener el ID que la DB le asignó automáticamente
    return db_user

# --- 2. LEER (READ) ---
def get_user(db: Session, user_id: int):
    # Buscamos directamente por la llave primaria (ID).
    # Si no existe, devolverá None.
    return db.get(User, user_id)

# --- 3. ACTUALIZAR (UPDATE) ---
def update_user(db: Session, user_id: int, user_in: UserUpdate):
    # Primero buscamos si el usuario existe antes de intentar editarlo.
    db_user = db.get(User, user_id)
    if not db_user:
        return None

    # 'exclude_unset=True' es la clave: hace que solo se actualicen
    # los campos que el usuario envió en la petición.
    update_data = user_in.model_dump(exclude_unset=True)

    # Si el usuario decidió cambiar su contraseña, procesamos el nuevo hash.
    if "password" in update_data:
        # Quitamos "password" del diccionario y guardamos el hash en "password_hash"
        update_data["password_hash"] = update_data.pop("password") + "hashed"

    # sqlmodel_update aplica los cambios del diccionario al objeto de la DB automáticamente.
    db_user.sqlmodel_update(update_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- 4. BORRAR (DELETE) ---
def delete_user(db: Session, user_id: int):
    db_user = db.get(User, user_id)
    if db_user:
        db.delete(db_user) # Marcamos para borrar
        db.commit()        # Confirmamos el borrado en la DB
        return True
    return False # Si no existía, avisamos que no hubo nada que borrar