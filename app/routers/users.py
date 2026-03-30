import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import user_service

# Todas las rutas tendrán el prefijo "/users" (ej: http://localhost:8000/themes/)
# y aparecerán agrupadas bajo la etiqueta "Users" en Swagger.
router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate):
    # Recibe el esquema UserCreate (que incluye la contraseña en texto plano)
    # y lo envía al servicio. Allí es donde se tendrá que encriptar antes de guardar.
    return await user_service.create_user(user)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    # Busca un usuario por su ID numérico.
    # El 'response_model=UserOut' es tu escudo aquí: asegura que el
    # 'password_hash' jamás se envíe al cliente, solo datos públicos.
    # Fíjate en el 'await', clave en operaciones asíncronas con MongoDB
    db_user = await user_service.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserUpdate):
    # Actualiza datos básicos del usuario (nombre, email, etc.).
    updated_user = await user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    # Elimina permanentemente al usuario del sistema.
    if not await user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente."}

# Esta ruta no recibe JSON, recibe un archivo binario a través de un formulario.
@router.post("/{user_id}/photo", response_model=UserOut)
async def upload_user_photo(user_id: int, file: UploadFile = File(...)):
    # Endpoint dedicado exclusivamente a subir y guardar la foto de perfil.
    # Comprobamos si el usuario existe antes de guardar nada.
    # Así evitamos llenar el disco duro de archivos inutiles.
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Generamos la ruta donde se va a guardar la imagen físicamente.
    # Al ponerle "user_{user_id}_" al inicio, evitamos que si dos usuarios
    # suben una foto llamada "foto.jpg", se sobrescriban entre sí.
    file_name = f"user_{user_id}_{file.filename}"

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
    updated_user = await user_service.update_user_photo(user_id, photo_url)

    # Devolvemos el usuario actualizado para que el frontend pueda pintar la nueva foto.
    return updated_user