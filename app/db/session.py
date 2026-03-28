from sqlalchemy import URL
from sqlmodel import create_engine, Session
from app.core.config import config

# --- LÓGICA DE CONEXIÓN ADAPTADA ---
connect_args = {}

if config.db_type.startswith("sqlite"):
    # Si es SQLite, necesitamos este argumento para hilos concurrentes
    connect_args = {"check_same_thread": False}
    database_url = "sqlite:///./database.db"
else:
    # Si es Postgres, construimos la URL profesionalmente
    connect_args = {} # Postgres gestiona los hilos nativamente
    database_url = URL.create(
        drivername=config.db_type,
        username=config.db_user,
        password=config.db_password,
        host=config.db_host,
        port=int(config.db_port),
        database=config.db_name,
    )

# Creamos el engine con la URL decidida
engine = create_engine(
    database_url,
    echo=config.debug,
    connect_args=connect_args
)

def get_session():
    with Session(engine) as session:
        yield session