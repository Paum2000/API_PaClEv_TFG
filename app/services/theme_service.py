from sqlmodel import Session, select
from app.models.theme import Theme, ThemeCreate, ThemeUpdate

def create_theme(db: Session, theme_in: ThemeCreate):
    db_theme = Theme.model_validate(theme_in)
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

def get_all_themes(db: Session):
    statement = select(Theme)
    return db.exec(statement).all()

def update_theme(db: Session, theme_id: int, theme_in: ThemeUpdate):
    db_theme = db.get(Theme, theme_id)
    if not db_theme:
        return None

    update_data = theme_in.model_dump(exclude_unset=True)
    db_theme.sqlmodel_update(update_data)

    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

def delete_theme(db: Session, theme_id: int):
    db_theme = db.get(Theme, theme_id)
    if db_theme:
        db.delete(db_theme)
        db.commit()
        return True
    return False