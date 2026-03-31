import pytest
import pymongo
from fastapi.testclient import TestClient
from app.main import app

# Configuramos el cliente de pruebas.
# Lo creamos solo una vez por archivo (scope="module") para que los tests vayan más rápido.
@pytest.fixture(scope="module")
def client():
    # Creamos un cliente "falso" para poder probar la API sin tener que arrancar el servidor de verdad.
    with TestClient(app) as c:
        yield c

# Esto se ejecuta solo (autouse=True) antes de cada test para no mezclar datos.
@pytest.fixture(autouse=True)
def clear_database():
    # Se conecta a la base de datos que usamos exclusivamente para hacer pruebas
    sync_client = pymongo.MongoClient("mongodb://mongo_test:27017")
    db = sync_client["agenda_testing_db"]

    # Recorre todo lo que hay guardado y lo borra.
    # Así nos aseguramos de empezar cada test con la base de datos limpia.
    for collection in db.list_collection_names():
        db[collection].delete_many({})

    # Cerramos la conexión para no dejar nada colgado.
    sync_client.close()