from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.user import UserCreate, UserOut, UserUpdate
from app.services import user_service
from app.db.session import get_session

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    return user_service.create_user(db, user)

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_session)):
    db_user = user_service.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    updated_user = user_service.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_session)):
    if not user_service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente."}

import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
# ... (tus otras importaciones)

@router.post("/{user_id}/photo")
def upload_user_photo(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_session)):
    # 1. Comprobamos que el usuario existe
    db_user = user_service.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Definimos dónde se va a guardar y con qué nombre
    # Usamos el user_id en el nombre para que no se sobrescriban fotos de distintos usuarios
    file_name = f"user_{user_id}_{file.filename}"
    file_path = os.path.join("app", "static", "uploads", file_name)

    # 3. Guardamos el archivo físico en el disco duro
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Actualizamos la base de datos con la ruta de la foto
    # La ruta pública será /static/uploads/nombre_del_archivo.jpg
    db_user.user_photo = f"/static/uploads/{file_name}"
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Foto subida con éxito", "photo_url": db_user.user_photo}