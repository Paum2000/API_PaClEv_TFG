from fastapi.testclient import TestClient

def test_create_theme_exito(client: TestClient):
    response = client.post("/themes/", json={"name": "Modo Oscuro"})
    assert response.status_code == 200
    assert response.json()["name"] == "Modo Oscuro"

def test_get_themes(client: TestClient):
    client.post("/themes/", json={"name": "Modo Claro"})
    response = client.get("/themes/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_theme(client: TestClient):
    res_create = client.post("/themes/", json={"name": "Azul"})
    theme_id = res_create.json()["id"]

    res_update = client.put(f"/themes/{theme_id}", json={"name": "Rojo"})
    assert res_update.status_code == 200
    assert res_update.json()["name"] == "Rojo"

def test_delete_theme(client: TestClient):
    res_create = client.post("/themes/", json={"name": "Borrable"})
    theme_id = res_create.json()["id"]

    res_delete = client.delete(f"/themes/{theme_id}")
    assert res_delete.status_code == 200

    res_get = client.delete(f"/themes/{theme_id}") # Intentar borrar de nuevo da 404
    assert res_get.status_code == 404