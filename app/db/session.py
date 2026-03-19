from sqlmodel import Session, create_engine
from app.core.setting import settings

connect_args = {"check_same_thread": False}
database_url = "sqlite:///./" + settings.database_name

engine = create_engine(
    database_url,
    echo=settings.debug,
    connect_args=connect_args
)

def get_session():
    with Session(engine) as session:
        yield session