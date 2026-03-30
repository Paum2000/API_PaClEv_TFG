from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.theme import ThemeCreate, ThemeOut, ThemeUpdate
from app.services import theme_service

# Todas las rutas tendrán el prefijo "/themes" (ej: http://localhost:8000/themes/)
# y aparecerán agrupadas bajo la etiqueta "Themes" en Swagger.
router = APIRouter(prefix="/themes", tags=["Themes"])

@router.post("/", response_model=ThemeOut)
async def create_theme(theme: ThemeCreate):
    # Recibe el esquema ThemeCreate (que solo exige el 'name')
    # y lo envía al servicio para guardarlo como un nuevo documento en MongoDB.
    return await theme_service.create_theme(theme)

# response_model=List[ThemeOut]: Devuelve un arreglo con todos los temas.
@router.get("/", response_model=List[ThemeOut])
async def get_all_themes():
    # A diferencia de las tareas que se filtran por /user/{user_id},
    # aquí obtenemos todos los temas de la base de datos.
    # Esto es ideal para que el frontend pueda llenar un menú desplegable (dropdown)
    # y el usuario elija qué tema quiere aplicar a su configuración.
    return await theme_service.get_all_themes()

@router.put("/{theme_id}", response_model=ThemeOut)
async def update_theme(theme_id: int, theme: ThemeUpdate):
    # Permite modificar un tema existente.
    # Busca por el 'theme_id' global.
    updated_theme = await theme_service.update_theme(theme_id, theme)

    # Si el servicio devuelve None (el tema no existe), lanzamos un error 404.
    if not updated_theme:
        raise HTTPException(status_code=404, detail="Tema no encontrado")

    return updated_theme

@router.delete("/{theme_id}")
async def delete_theme(theme_id: int):
    # Elimina un tema de la base de datos global.
    if not await theme_service.delete_theme(theme_id):
        raise HTTPException(status_code=404, detail="Tema no encontrado")

    return {"message": "Tema eliminado correctamente."}