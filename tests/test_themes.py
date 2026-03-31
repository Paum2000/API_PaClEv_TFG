from fastapi.testclient import TestClient

# --- TEST 1: Crear un tema nuevo ---
def test_create_theme_exito(client: TestClient):
    # Mandamos los datos para crear un tema (ej: "Modo Oscuro").
    response = client.post("/themes/", json={"name": "Modo Oscuro"})

    # Verificamos que la API da el OK (200) y que el nombre devuelto coincide.
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Modo Oscuro"

    # Nos aseguramos de que la base de datos realmente le asignó un ID, buscando por "id" o "_id".
    theme_id = data.get("id") or data.get("_id")
    assert theme_id is not None


# --- TEST 2: Listar todos los temas ---
def test_get_themes(client: TestClient):
    # Primero creamos un tema ("Modo Claro") a mano para asegurarnos de que la lista no venga vacía.
    client.post("/themes/", json={"name": "Modo Claro"})

    # Pedimos a la API que nos traiga todos los temas guardados.
    response = client.get("/themes/")
    assert response.status_code == 200

    # Comprobamos que efectivamente devuelve una lista y que tiene al menos el elemento que acabamos de crear.
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# --- TEST 3: Editar un tema existente ---
def test_update_theme(client: TestClient):
    # Creamos un tema de prueba ("Azul") y sacamos su ID para saber cuál editar.
    res_create = client.post("/themes/", json={"name": "Azul"})
    theme_id = res_create.json().get("id") or res_create.json().get("_id")

    # Le pasamos a la API los nuevos datos (cambiamos "Azul" por "Rojo").
    res_update = client.put(f"/themes/{theme_id}", json={"name": "Rojo"})

    # Confirmamos que no hay errores y que el nombre se ha actualizado correctamente en la respuesta.
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "Rojo"


# --- TEST 4: Borrar un tema y comprobar que desaparece ---
def test_delete_theme(client: TestClient):
    # 1. Preparamos el terreno creando un tema destinado a ser borrado y nos guardamos su ID.
    res_create = client.post("/themes/", json={"name": "Borrable"})
    theme_id = res_create.json().get("id") or res_create.json().get("_id")

    # 2. Damos la orden de eliminarlo. El código 200 nos dice que se borró con éxito la primera vez.
    res_delete = client.delete(f"/themes/{theme_id}")
    assert res_delete.status_code == 200

    # 3. La prueba de fuego: intentamos borrar el MISMO tema de nuevo.
    # Como ya se borró en el paso anterior y no existe, la API nos tiene que soltar un error 404 (Not Found).
    res_get = client.delete(f"/themes/{theme_id}")
    assert res_get.status_code == 404