from fastapi import APIRouter, HTTPException
from typing import List

from app.models.theme import ThemeCreate, ThemeOut, ThemeUpdate
from app.services import theme_service

router = APIRouter(prefix="/themes", tags=["Themes"])

@router.post("/", response_model=ThemeOut)
async def create_theme(theme: ThemeCreate):
    return await theme_service.create_theme(theme)

@router.get("/", response_model=List[ThemeOut])
async def get_all_themes():
    return await theme_service.get_all_themes()

@router.put("/{theme_id}", response_model=ThemeOut)
async def update_theme(theme_id: int, theme: ThemeUpdate):
    updated_theme = await theme_service.update_theme(theme_id, theme)
    if not updated_theme:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return updated_theme

@router.delete("/{theme_id}")
async def delete_theme(theme_id: int):
    if not await theme_service.delete_theme(theme_id):
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return {"message": "Tema eliminado correctamente."}