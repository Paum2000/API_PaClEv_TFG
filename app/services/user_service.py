from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserUpdate

def create_user(db: Session, user_in: UserCreate):
    # En un entorno real, aquí hashearías la contraseña antes de guardarla
    db_user = User(
        user_name=user_in.user_name,
        email=user_in.email,
        birthday=user_in.birthday,
        user_photo=user_in.user_photo,
        password_hash=user_in.password + "hashed" # <--- Simulación de hash
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.get(User, user_id)

def update_user(db: Session, user_id: int, user_in: UserUpdate):
    db_user = db.get(User, user_id)
    if not db_user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        # Aquí también hashearías si envían nueva password
        update_data["password_hash"] = update_data.pop("password") + "hashed"

    db_user.sqlmodel_update(update_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.get(User, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False