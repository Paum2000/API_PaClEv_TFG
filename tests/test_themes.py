from fastapi.testclient import TestClient

def test_create_theme_exito(client: TestClient):
    response = client.post("/themes/", json={"name": "Modo Oscuro"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Modo Oscuro"
    # Verificamos que se generó el ID (capturando ambos posibles nombres)
    theme_id = data.get("id") or data.get("_id")
    assert theme_id is not None

def test_get_themes(client: TestClient):
    # Creamos uno para asegurar que la lista no esté vacía
    client.post("/themes/", json={"name": "Modo Claro"})
    response = client.get("/themes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_theme(client: TestClient):
    res_create = client.post("/themes/", json={"name": "Azul"})
    # Capturamos el ID dinámico con doble comprobación
    theme_id = res_create.json().get("id") or res_create.json().get("_id")

    res_update = client.put(f"/themes/{theme_id}", json={"name": "Rojo"})
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "Rojo"

def test_delete_theme(client: TestClient):
    # 1. Creamos el tema
    res_create = client.post("/themes/", json={"name": "Borrable"})
    theme_id = res_create.json().get("id") or res_create.json().get("_id")

    # 2. Borramos el tema
    res_delete = client.delete(f"/themes/{theme_id}")
    assert res_delete.status_code == 200

    # 3. Intentar borrar de nuevo debe dar 404
    # Usamos el mismo ID que acabamos de borrar para asegurar la inexistencia
    res_get = client.delete(f"/themes/{theme_id}")
    assert res_get.status_code == 404