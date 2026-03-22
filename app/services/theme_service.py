from sqlmodel import Session, select
from app.models.theme import Theme, ThemeCreate, ThemeUpdate

# --- 1. CREAR (CREATE) ---
def create_theme(db: Session, theme_in: ThemeCreate):
    # 'model_validate' es una forma elegante de convertir los datos
    # de entrada (ThemeCreate) al formato de la tabla (Theme).
    db_theme = Theme.model_validate(theme_in)

    db.add(db_theme)      # Agregamos el nuevo tema a la sesión
    db.commit()          # Guardamos en la base de datos
    db.refresh(db_theme)  # Obtenemos el ID generado
    return db_theme

# --- 2. LEER TODOS (READ ALL) ---
def get_all_themes(db: Session):
    # A diferencia del usuario, aquí queremos una lista de todos los temas.
    # 'select(Theme)' es como escribir "SELECT * FROM themes" en SQL.
    statement = select(Theme)
    # 'db.exec' ejecuta la orden y '.all()' nos da una lista.
    return db.exec(statement).all()

# --- 3. ACTUALIZAR (UPDATE) ---
def update_theme(db: Session, theme_id: int, theme_in: ThemeUpdate):
    # Buscamos el tema por su ID único.
    db_theme = db.get(Theme, theme_id)
    if not db_theme:
        return None # Si no existe, devolvemos None.

    # Extraemos solo los campos que el usuario envió.
    update_data = theme_in.model_dump(exclude_unset=True)

    # Actualizamos el objeto de la base de datos con los nuevos datos.
    db_theme.sqlmodel_update(update_data)

    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    return db_theme

# --- 4. BORRAR (DELETE) ---
def delete_theme(db: Session, theme_id: int):
    # Primero buscamos si el tema existe.
    db_theme = db.get(Theme, theme_id)
    if db_theme:
        db.delete(db_theme) # Orden de eliminación
        db.commit()         # Ejecución del borrado
        return True
    return False # Si no existe, retornamos False