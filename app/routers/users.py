import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    return await user_service.create_user(user)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    # Fíjate en el 'await', clave en MongoDB
    db_user = await user_service.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate):
    updated_user = await user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    if not await user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente."}

@router.post("/{user_id}/photo", response_model=UserOut)
async def upload_user_photo(user_id: int, file: UploadFile = File(...)):
    # 1. Comprobamos si el usuario existe ANTES de guardar nada
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Generamos la ruta donde se va a guardar la imagen
    # Ej: app/static/uploads/user_1_mifoto.jpg
    file_name = f"user_{user_id}_{file.filename}"
    file_path = os.path.join("app", "static", "uploads", file_name)

    # 3. Guardamos el archivo físicamente en el disco duro
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. Actualizamos la base de datos usando
    photo_url = f"/static/uploads/{file_name}"
    updated_user = await user_service.update_user_photo(user_id, photo_url)

    # Devolvemos el usuario actualizado
    return updated_user