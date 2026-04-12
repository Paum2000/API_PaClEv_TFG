import pytest
import pymongo
import os
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

@pytest.fixture
def normal_user_token_headers(client):
    # Crea un usuario normal, inicia sesión y devuelve la cabecera HTTP con el Token.
    # 1. Registramos al usuario de prueba a través de tu API
    client.post("/users/", json={
        "user_name": "Usuario Test",
        "email": "normal@test.com",
        "password": "password123"
    })

    # 2. Iniciamos sesión (Fíjate que OAuth2 usa 'data', no 'json')
    response = client.post("/auth/login", data={
        "username": "normal@test.com",
        "password": "password123"
    })

    # 3. Extraemos el token y montamos la cabecera exacta que espera FastAPI
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_token_headers(client):
    # Crea un usuario, lo convierte en Admin "por debajo de la mesa" y devuelve su Token.
    # 1. Registramos al usuario por la API
    client.post("/users/", json={
        "user_name": "Admin Test",
        "email": "admin@test.com",
        "password": "adminpassword"
    })

    # 2. Truco de Hacker: Le damos superpoderes directamente en MongoDB
    sync_client = pymongo.MongoClient("mongodb://mongo_test:27017")
    db = sync_client["agenda_testing_db"]
    db.users.update_one({"email": "admin@test.com"}, {"$set": {"is_admin": True}})
    sync_client.close()

    # 3. Iniciamos sesión
    response = client.post("/auth/login", data={
        "username": "admin@test.com",
        "password": "adminpassword"
    })

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}