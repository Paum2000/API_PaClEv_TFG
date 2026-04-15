import os
import shutil
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service
from app.core.security import get_current_user
from app.models.user import User

# Todas las rutas tendrán el prefijo "/users" (ej: http://localhost:8000/themes/)
# y aparecerán agrupadas bajo la etiqueta "Users" en Swagger.
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    # Recibe el esquema UserCreate (que incluye la contraseña en texto plano)
    # y lo envía al servicio. Allí es donde se tendrá que encriptar antes de guardar.
    return await user_service.create_user(user)

@router.get("/me", response_model=UserOut)
async def get_user(current_user: User = Depends(get_current_user)):
    # El candado ya busca al usuario en la base de datos por ti.
    # Así que simplemente devolvemos el usuario actual
    return current_user

@router.put("/me", response_model=UserOut)
async def update_user(
        user: UserUpdate,
        current_user: User = Depends(get_current_user)
):
    # Actualiza datos básicos del usuario (nombre, email, etc.).
    updated_user = await user_service.update_user(current_user.id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/me")
async def delete_user(
        current_user: User = Depends(get_current_user)
):
    # Elimina permanentemente al usuario del sistema.
    if not await user_service.delete_user(current_user.id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente."}

# Esta ruta no recibe JSON, recibe un archivo binario a través de un formulario.
@router.post("/me/photo", response_model=UserOut)
async def upload_user_photo(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user)
):
    # Generamos la ruta donde se va a guardar la imagen físicamente.
    # Al ponerle "user_{user_id}_" al inicio, evitamos que si dos usuarios
    # suben una foto llamada "foto.jpg", se sobrescriban entre sí.
    file_name = f"user_{current_user.id}_{file.filename}"

    # os.path.join arma la ruta correctamente dependiendo del sistema operativo
    # Ej: app/static/uploads/user_1_mifoto.jpg
    file_path = os.path.join("app", "static", "uploads", file_name)

    # Guardamos el archivo en el disco duro del servidor.
    # "wb" significa Write Binary (escribir en formato binario).
    with open(file_path, "wb") as buffer:
        # shutil.copyfileobj es súper eficiente porque copia el archivo
        # en pequeños trozos (chunks), evitando colapsar la memoria RAM.
        shutil.copyfileobj(file.file, buffer)

    # Generamos la ruta relativa que usará el frontend.
    # Esta es la URL pública que se guardará en MongoDB.
    photo_url = f"/static/uploads/{file_name}"

    # Llamamos a una función específica del servicio para actualizar solo este campo.
    updated_user = await user_service.update_user_photo(current_user.id, photo_url)

    # Devolvemos el usuario actualizado para que el frontend pueda pintar la nueva foto.
    return updated_user

@router.get("/", response_model=List[UserOut])
async def get_all_users(current_user: User = Depends(get_current_user)):
    # Obtiene el listado completo de usuarios de la aplicación.

    return await user_service.get_all_users()