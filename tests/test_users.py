from fastapi.testclient import TestClient

# --- 1. TESTS DE CREACIÓN (POST) ---

def test_create_user_exito(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "user_name": "Juan Perez",
            "email": "juan@example.com",
            "password": "mi_password_seguro",
            "birthday": "1995-05-15T00:00:00"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "juan@example.com"

    # Captura dinámica: intentamos 'id' primero (salida API) y '_id' como respaldo
    user_id = data.get("id") or data.get("_id")
    assert user_id is not None

def test_create_user_falta_campo_obligatorio(client: TestClient):
    response = client.post(
        "/users/",
        json={"user_name": "Incompleto", "password": "123"}
    )
    assert response.status_code == 422

# --- 2. TESTS DE LECTURA (GET) ---

def test_get_user_exito(client: TestClient):
    response_create = client.post(
        "/users/",
        json={"user_name": "Ana", "email": "ana@test.com", "password": "123"}
    )
    data = response_create.json()
    user_id = data.get("id") or data.get("_id")

    response_get = client.get(f"/users/{user_id}")
    assert response_get.status_code == 200
    assert response_get.json()["email"] == "ana@test.com"

def test_get_user_no_existe(client: TestClient):
    id_falso = 9999999999999
    response = client.get(f"/users/{id_falso}")
    assert response.status_code == 404

# --- 3. TESTS DE ACTUALIZACIÓN (PUT) ---

def test_update_user_exito(client: TestClient):
    response_create = client.post(
        "/users/",
        json={"user_name": "Carlos", "email": "carlos@test.com", "password": "123"}
    )
    data = response_create.json()
    user_id = data.get("id") or data.get("_id")

    response_update = client.put(
        f"/users/{user_id}",
        json={"user_name": "Carlos Modificado"}
    )
    assert response_update.status_code == 200
    assert response_update.json()["user_name"] == "Carlos Modificado"

# --- 4. TESTS DE ELIMINACIÓN (DELETE) ---

def test_delete_user_exito(client: TestClient):
    response_create = client.post(
        "/users/",
        json={"user_name": "Borrable", "email": "borrar@test.com", "password": "123", "birthday": "1995-05-15T00:00:00"}
    )
    data = response_create.json()

    # ESTO NOS DIRÁ LA VERDAD EN LA CONSOLA:
    print(f"\n DEBUG DATA: {data}")

    # Intentamos capturar el ID de todas las formas posibles
    user_id = data.get("id") or data.get("_id") or data.get("user_id")

    response_delete = client.delete(f"/users/{user_id}")
    assert response_delete.status_code == 200

def test_upload_user_photo(client: TestClient):
    response_create = client.post(
        "/users/",
        json={"user_name": "Fotografo", "email": "foto@test.com", "password": "123"}
    )
    data = response_create.json()
    user_id = data.get("id") or data.get("_id")

    archivos = {"file": ("mi_cara.jpg", b"fake_data", "image/jpeg")}
    response_upload = client.post(f"/users/{user_id}/photo", files=archivos)

    assert response_upload.status_code == 200
    assert "user_photo" in response_upload.json()