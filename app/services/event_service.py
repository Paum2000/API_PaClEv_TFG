from sqlmodel import Session, select
from app.models.event import Event, EventCreate, EventUpdate

# --- 1. CREAR EVENTO (CREATE) ---
def create_event(db: Session, event_in: EventCreate):
    # 'model_validate' transforma los datos que vienen del cliente (EventCreate)
    # en una fila lista para la tabla 'events'.
    db_event = Event.model_validate(event_in)

    db.add(db_event)      # Registramos el evento en la sesión
    db.commit()          # Impactamos los cambios en la base de datos
    db.refresh(db_event)  # Recuperamos el objeto con su ID generado
    return db_event

# --- 2. LEER EVENTOS POR USUARIO (READ) ---
def get_user_events(db: Session, user_id: int):
    # Filtramos la consulta para traer solo los eventos de un usuario específico.
    # Es importante para la privacidad: SELECT * FROM events WHERE user_id = ...
    statement = select(Event).where(Event.user_id == user_id)

    # '.all()' nos devuelve una lista con todos los eventos encontrados.
    return db.exec(statement).all()

# --- 3. ACTUALIZAR EVENTO (UPDATE) ---
def update_event(db: Session, event_id: int, event_in: EventUpdate):
    # Primero verificamos si el evento realmente existe en la DB.
    db_event = db.get(Event, event_id)
    if not db_event:
        return None

    # 'exclude_unset=True' permite que si el usuario solo cambia la hora de inicio,
    # el título y la descripción se queden igual.
    update_data = event_in.model_dump(exclude_unset=True)

    # Sincronizamos los cambios del diccionario con el objeto de la DB.
    db_event.sqlmodel_update(update_data)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# --- 4. BORRAR EVENTO (DELETE) ---
def delete_event(db: Session, event_id: int):
    # Buscamos el evento antes de intentar borrar.
    db_event = db.get(Event, event_id)
    if db_event:
        db.delete(db_event) # Marcamos para eliminar
        db.commit()         # Confirmamos la eliminación definitiva
        return True
    return False # Si no existía, avisamos que no se borró nada