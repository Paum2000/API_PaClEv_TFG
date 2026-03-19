from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.models.theme import ThemeCreate, ThemeOut, ThemeUpdate
from app.services import theme_service
from app.db.session import get_session

router = APIRouter(prefix="/themes", tags=["Themes"])

@router.post("/", response_model=ThemeOut)
def create_theme(theme: ThemeCreate, db: Session = Depends(get_session)):
    return theme_service.create_theme(db, theme)

@router.get("/", response_model=List[ThemeOut])
def get_all_themes(db: Session = Depends(get_session)):
    return theme_service.get_all_themes(db)

@router.put("/{theme_id}", response_model=ThemeOut)
def update_theme(theme_id: int, theme: ThemeUpdate, db: Session = Depends(get_session)):
    updated_theme = theme_service.update_theme(db, theme_id, theme)
    if not updated_theme:
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return updated_theme

@router.delete("/{theme_id}")
def delete_theme(theme_id: int, db: Session = Depends(get_session)):
    if not theme_service.delete_theme(db, theme_id):
        raise HTTPException(status_code=404, detail="Tema no encontrado")
    return {"message": "Tema eliminado correctamente."}