from fastapi import APIRouter
from typing import List
from app.schemas.theme import ThemeCreate, ThemeOut, ThemeUpdate

router = APIRouter(prefix="/themes", tags=["Themes"])

@router.post("/", response_model=ThemeOut)
def create_theme(theme: ThemeCreate):
    return {"message": "Endpoint listo. Lógica pendiente en ramas."}

@router.get("/", response_model=List[ThemeOut])
def get_all_themes():
    return [{"message": "Endpoint listo. Lógica pendiente en ramas."}]

@router.put("/{theme_id}", response_model=ThemeOut)
def update_theme(theme_id: int, theme: ThemeUpdate):
    return {"message": "Endpoint de edición listo. Lógica pendiente."}

@router.delete("/{theme_id}")
def delete_theme(theme_id: int):
    return {"message": f"Tema {theme_id} eliminado. Lógica pendiente."}