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
    assert data["user_name"] == "Juan Perez"
    assert "id" in data # Comprobamos que la BD le ha asignado un ID

def test_create_user_falta_campo_obligatorio(client: TestClient):
    # Intentamos crear sin enviar el email (que es obligatorio)
    response = client.post(
        "/users/",
        json={
            "user_name": "Incompleto",
            "password": "123"
        }
    )
    # 422 Unprocessable Entity es el error estándar de validación de Pydantic
    assert response.status_code == 422

# --- 2. TESTS DE LECTURA (GET) ---

def test_get_user_exito(client: TestClient):
    # Primero creamos un usuario
    response_create = client.post(
        "/users/",
        json={"user_name": "Ana", "email": "ana@test.com", "password": "123"}
    )
    user_id = response_create.json()["id"]

    # Luego intentamos obtenerlo
    response_get = client.get(f"/users/{user_id}")
    assert response_get.status_code == 200
    assert response_get.json()["email"] == "ana@test.com"

def test_get_user_no_existe(client: TestClient):
    # Buscamos un ID que sabemos que no existe en una BD recién creada
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

# --- 3. TESTS DE ACTUALIZACIÓN (PUT) ---

def test_update_user_exito(client: TestClient):
    # Creamos
    response_create = client.post(
        "/users/",
        json={"user_name": "Carlos", "email": "carlos@test.com", "password": "123"}
    )
    user_id = response_create.json()["id"]

    # Actualizamos solo el nombre
    response_update = client.put(
        f"/users/{user_id}",
        json={"user_name": "Carlos Modificado"}
    )
    assert response_update.status_code == 200
    assert response_update.json()["user_name"] == "Carlos Modificado"
    assert response_update.json()["email"] == "carlos@test.com" # El email no debería haber cambiado

def test_update_user_no_existe(client: TestClient):
    response = client.put("/users/9999", json={"user_name": "Fantasma"})
    assert response.status_code == 404

# --- 4. TESTS DE ELIMINACIÓN (DELETE) ---

def test_delete_user_exito(client: TestClient):
    # Creamos
    response_create = client.post(
        "/users/",
        json={"user_name": "Borrable", "email": "borrar@test.com", "password": "123"}
    )
    user_id = response_create.json()["id"]

    # Borramos
    response_delete = client.delete(f"/users/{user_id}")
    assert response_delete.status_code == 200

    # Comprobamos que ya no existe
    response_get = client.get(f"/users/{user_id}")
    assert response_get.status_code == 404

def test_delete_user_no_existe(client: TestClient):
    response = client.delete("/users/9999")
    assert response.status_code == 404

def test_upload_user_photo(client: TestClient):
    # 1. Primero creamos un usuario
    response_create = client.post(
        "/users/",
        json={"user_name": "Fotografo", "email": "foto@test.com", "password": "123"}
    )
    user_id = response_create.json()["id"]

    # 2. Simulamos el contenido de una imagen en binario
    # No necesitamos una imagen real, solo un puñado de bytes simulando ser un archivo
    contenido_falso_imagen = b"esto_es_una_imagen_falsa_en_bytes"

    # Preparamos el archivo para enviarlo (nombre del campo, tupla con: nombre de archivo, contenido, tipo MIME)
    archivos = {
        "file": ("mi_cara.jpg", contenido_falso_imagen, "image/jpeg")
    }

    # 3. Hacemos la petición POST enviando el archivo
    response_upload = client.post(f"/users/{user_id}/photo", files=archivos)

    # 4. Comprobaciones
    assert response_upload.status_code == 200
    datos = response_upload.json()
    assert datos["message"] == "Foto subida con éxito"
    assert "mi_cara.jpg" in datos["photo_url"]

    # 5. Comprobamos que el usuario en DB se ha actualizado
    response_get = client.get(f"/users/{user_id}")
    assert response_get.json()["user_photo"] == datos["photo_url"]