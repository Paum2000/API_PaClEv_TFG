import os
import pytest
import pymongo
from fastapi.testclient import TestClient
from app.main import app

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://mongo_test:27017")

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def clear_database():
    # Le ponemos 5 segundos de límite (5000ms) para que falle rápido si no hay conexión
    sync_client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = sync_client["agenda_testing_db"]
    for collection in db.list_collection_names():
        db[collection].delete_many({})
    sync_client.close()

@pytest.fixture
def normal_user_token_headers(client):
    client.post("/users/", json={
        "user_name": "Usuario Test",
        "nickname": "usuario_normal",
        "email": "normal@test.com",
        "password": "password123"
    })

    response = client.post("/auth/login", data={
        "username": "normal@test.com",
        "password": "password123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_token_headers(client):
    client.post("/users/", json={
        "user_name": "Admin Test",
        "nickname": "super_admin",
        "email": "admin@test.com",
        "password": "adminpassword"
    })

    # Usamos la variable dinámica aquí también
    sync_client = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = sync_client["agenda_testing_db"]
    db.users.update_one({"email": "admin@test.com"}, {"$set": {"is_admin": True}})
    sync_client.close()

    response = client.post("/auth/login", data={
        "username": "admin@test.com",
        "password": "adminpassword"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}