from fastapi.testclient import TestClient

# --- TEST 1: Crear un tema nuevo ---
def test_create_theme_exito(client: TestClient, admin_token_headers):
    # Mandamos los datos usando nuestra llave de Administrador.
    response = client.post(
        "/themes/",
        json={"name": "Modo Oscuro"},
        headers=admin_token_headers
    )

    # Verificamos que la API da el OK (200) y que el nombre devuelto coincide.
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Modo Oscuro"

    # Nos aseguramos de que la base de datos realmente le asignó un ID.
    theme_id = data.get("id") or data.get("_id")
    assert theme_id is not None


# --- TEST 2: Listar todos los temas ---
def test_get_themes(client: TestClient, admin_token_headers):
    # 1. El administrador crea un tema a mano para que la lista no venga vacía.
    client.post(
        "/themes/",
        json={"name": "Modo Claro"},
        headers=admin_token_headers
    )

    # 2. PÚBLICO: Pedimos a la API que nos traiga todos los temas.
    # ¡Fíjate que NO le pasamos headers aquí porque esta ruta es libre!
    response = client.get("/themes/")
    assert response.status_code == 200

    # Comprobamos que efectivamente devuelve una lista y que tiene al menos el elemento.
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# --- TEST 3: Editar un tema existente ---
def test_update_theme(client: TestClient, admin_token_headers):
    # Creamos un tema de prueba ("Azul") con nuestro admin.
    res_create = client.post(
        "/themes/",
        json={"name": "Azul"},
        headers=admin_token_headers
    )
    theme_id = res_create.json().get("id") or res_create.json().get("_id")

    # Le pasamos a la API los nuevos datos (cambiamos "Azul" por "Rojo") usando la llave.
    res_update = client.put(
        f"/themes/{theme_id}",
        json={"name": "Rojo"},
        headers=admin_token_headers
    )

    # Confirmamos que no hay errores y que el nombre se ha actualizado correctamente.
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "Rojo"


# --- TEST 4: Borrar un tema y comprobar que desaparece ---
def test_delete_theme(client: TestClient, admin_token_headers):
    # 1. Preparamos el terreno creando el tema como Admin.
    res_create = client.post(
        "/themes/",
        json={"name": "Borrable"},
        headers=admin_token_headers
    )
    theme_id = res_create.json().get("id") or res_create.json().get("_id")

    # 2. Damos la orden de eliminarlo usando nuestros privilegios.
    res_delete = client.delete(
        f"/themes/{theme_id}",
        headers=admin_token_headers
    )
    assert res_delete.status_code == 200

    # 3. La prueba de fuego: intentamos borrarlo de nuevo para asegurar el 404.
    res_get = client.delete(
        f"/themes/{theme_id}",
        headers=admin_token_headers
    )
    assert res_get.status_code == 404