from fastapi.testclient import TestClient

# --- 1. TESTS DE CREACIÓN (POST) ---
# PÚBLICO: No necesitan token porque la gente tiene que poder registrarse.

def test_create_user_exito(client: TestClient):
    # Mando todos los datos necesarios para registrar un usuario nuevo.
    response = client.post(
        "/users/",
        json={
            "user_name": "Juan Perez",
            "email": "juan@example.com",
            "password": "mi_password_seguro",
            "birthday": "1995-05-15T00:00:00"
        }
    )

    # Verifico que la API me da el OK (200).
    assert response.status_code == 200
    data = response.json()

    # Compruebo que el email se ha guardado tal cual lo envié.
    assert data["email"] == "juan@example.com"

    # Nos aseguramos de que MongoDB le asignó un ID
    user_id = data.get("id") or data.get("_id")
    assert user_id is not None

def test_create_user_falta_campo_obligatorio(client: TestClient):
    # Intento crear un usuario a medias (falta el email, que es obligatorio).
    response = client.post(
        "/users/",
        json={"user_name": "Incompleto", "password": "123"}
    )
    # La API debe rechazarlo (422 Unprocessable Entity).
    assert response.status_code == 422


# --- 2. TESTS DE LECTURA (GET) ---
# PRIVADOS: Usamos nuestro token y la ruta /me

def test_get_user_me_exito(client: TestClient, normal_user_token_headers):
    # Le pido a la API que me devuelva "MI" perfil.
    # Como el token lo genera nuestro conftest.py, sabemos que el usuario se llama "normal@test.com"
    response_get = client.get("/users/me", headers=normal_user_token_headers)

    # Confirmo que entra (200) y que soy yo.
    assert response_get.status_code == 200
    assert response_get.json()["email"] == "normal@test.com"

def test_get_user_me_sin_token(client: TestClient):
    # Intento acceder a la ruta privada SIN mandarle la cabecera del token.
    response = client.get("/users/me")

    # La API debe bloquearme en la puerta con un 401 (Unauthorized).
    assert response.status_code == 401


# --- 3. TESTS DE ACTUALIZACIÓN (PUT) ---

def test_update_user_me_exito(client: TestClient, normal_user_token_headers):
    # Le mando una actualización cambiando solo el nombre de MI perfil.
    response_update = client.put(
        "/users/me",
        json={"user_name": "Carlos Modificado"},
        headers=normal_user_token_headers
    )

    # Verifico que acepta el cambio (200) y que en la respuesta el nombre ya sale actualizado.
    assert response_update.status_code == 200
    assert response_update.json()["user_name"] == "Carlos Modificado"


# --- 4. TESTS DE ELIMINACIÓN (DELETE) ---

def test_delete_user_me_exito(client: TestClient, normal_user_token_headers):
    # Le meto el hachazo a "mi propia cuenta" con el método DELETE usando el token.
    response_delete = client.delete("/users/me", headers=normal_user_token_headers)

    # Confirmo que se borró sin problemas.
    assert response_delete.status_code == 200


# --- 5. TEST DE SUBIDA DE ARCHIVOS ---

def test_upload_user_photo_me(client: TestClient, normal_user_token_headers):
    # Simulo un archivo de imagen en la RAM.
    archivos = {"file": ("mi_cara.jpg", b"fake_data", "image/jpeg")}

    # Subo la foto a mi perfil. Ojo: uso 'files=' y le paso los headers.
    response_upload = client.post(
        "/users/me/photo",
        files=archivos,
        headers=normal_user_token_headers
    )

    # Me aseguro de que el servidor tragó bien la imagen (200) y guardó la URL.
    assert response_upload.status_code == 200
    assert "user_photo" in response_upload.json()