import pytest
import pymongo
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    # Arranca FastAPI y ejecuta tu brillante lifespan
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clear_database():
    # 100% Síncrono, sin Beanie ni Motor. Solo PyMongo para limpiar.
    sync_client = pymongo.MongoClient("mongodb://mongo_test:27017")
    db = sync_client["agenda_testing_db"] # <- ¡Fíjate que usamos corchetes, no paréntesis!

    for collection in db.list_collection_names():
        db[collection].delete_many({})

    sync_client.close()