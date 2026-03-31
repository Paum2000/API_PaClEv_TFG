from fastapi.testclient import TestClient

# --- 1. TESTS DE CREACIÓN (POST) ---

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

    # Captura dinámica: busco el ID devuelto, ya sea como 'id' (salida normal) o '_id' (típico de MongoDB).
    user_id = data.get("id") or data.get("_id")
    assert user_id is not None

def test_create_user_falta_campo_obligatorio(client: TestClient):
    # Intento crear un usuario a medias (seguro falta el email, que es obligatorio).
    response = client.post(
        "/users/",
        json={"user_name": "Incompleto", "password": "123"}
    )
    # La API debe rechazarlo y quejarse con un error 422 (Unprocessable Entity) por faltar datos.
    assert response.status_code == 422


# --- 2. TESTS DE LECTURA (GET) ---

def test_get_user_exito(client: TestClient):
    # Primero creo un usuario de prueba para tener alguien a quien buscar.
    response_create = client.post(
        "/users/",
        json={"user_name": "Ana", "email": "ana@test.com", "password": "123"}
    )
    data = response_create.json()
    user_id = data.get("id") or data.get("_id")

    # Le pido a la API que me devuelva los datos de ese usuario en concreto usando su ID.
    response_get = client.get(f"/users/{user_id}")

    # Confirmo que lo encuentra (200) y que los datos coinciden con Ana.
    assert response_get.status_code == 200
    assert response_get.json()["email"] == "ana@test.com"

def test_get_user_no_existe(client: TestClient):
    # Me invento un ID que sé perfectamente que no existe en mi base de datos.
    id_falso = 9999999999999
    response = client.get(f"/users/{id_falso}")

    # La API debería soltar un 404 (Not Found) porque no hay nadie registrado con ese ID.
    assert response.status_code == 404


# --- 3. TESTS DE ACTUALIZACIÓN (PUT) ---

def test_update_user_exito(client: TestClient):
    # Creo el usuario original (Carlos) y me guardo su ID.
    response_create = client.post(
        "/users/",
        json={"user_name": "Carlos", "email": "carlos@test.com", "password": "123"}
    )
    data = response_create.json()
    user_id = data.get("id") or data.get("_id")

    # Le mando una actualización cambiando solo el nombre.
    response_update = client.put(
        f"/users/{user_id}",
        json={"user_name": "Carlos Modificado"}
    )

    # Verifico que acepta el cambio (200) y que en la respuesta el nombre ya sale actualizado.
    assert response_update.status_code == 200
    assert response_update.json()["user_name"] == "Carlos Modificado"


# --- 4. TESTS DE ELIMINACIÓN (DELETE) ---

def test_delete_user_exito(client: TestClient):
    # Creo un usuario que solo va a existir para ser borrado.
    response_create = client.post(
        "/users/",
        json={"user_name": "Borrable", "email": "borrar@test.com", "password": "123", "birthday": "1995-05-15T00:00:00"}
    )
    data = response_create.json()

    # ESTO NOS DIRÁ LA VERDAD EN LA CONSOLA:
    # Pongo un print estratégico para debugear y ver qué trae exactamente el JSON si ejecuto con 'pytest -s'.
    print(f"\n DEBUG DATA: {data}")

    # Intento capturar el ID de todas las formas posibles (por si algo fallaba antes).
    user_id = data.get("id") or data.get("_id") or data.get("user_id")

    # Le meto el hachazo al usuario con el método DELETE.
    response_delete = client.delete(f"/users/{user_id}")

    # Confirmo que se borró sin problemas.
    assert response_delete.status_code == 200


# --- 5. TEST DE SUBIDA DE ARCHIVOS ---

def test_upload_user_photo(client: TestClient):
    # Creo un usuario base al que le voy a asignar una foto de perfil.
    response_create = client.post(
        "/users/",
        json={"user_name": "Fotografo", "email": "foto@test.com", "password": "123"}
    )
    data = response_create.json()
    user_id = data.get("id") or data.get("_id")

    # Simulo un archivo de imagen en la RAM. Le pongo nombre, unos bytes falsos ("fake_data") y aviso que es un jpeg.
    archivos = {"file": ("mi_cara.jpg", b"fake_data", "image/jpeg")}

    # IMPORTANTE: Uso 'files=' en lugar de 'json=' para mandar la imagen en formato multipart/form-data.
    response_upload = client.post(f"/users/{user_id}/photo", files=archivos)

    # Me aseguro de que el servidor tragó bien la imagen (200) y me devolvió la clave de confirmación en el JSON.
    assert response_upload.status_code == 200
    assert "user_photo" in response_upload.json()