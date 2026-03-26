import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
from app.models.user import User
from app.models.task import Task
from app.models.event import Event
from app.models.theme import Theme
from app.models.setting import Setting
from app.main import app
from app.db.session import get_session

# Usamos SQLite en memoria
sqlite_url = "sqlite:///:memory:"
engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    # Crea las tablas
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Limpia la base de datos después de cada test
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    # Sobrescribimos la dependencia
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    yield client

    # Limpiamos la sobrescritura al terminar
    app.dependency_overrides.clear()