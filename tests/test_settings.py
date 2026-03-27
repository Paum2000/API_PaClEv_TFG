from fastapi.testclient import TestClient

def setup_entorno(client: TestClient):
    """Crea un usuario y un tema para poder crear una configuración"""
    res_u = client.post("/users/", json={"user_name": "SetUser", "email": "set@test.com", "password": "123"})
    res_t = client.post("/themes/", json={"name": "Tema Principal"})
    return res_u.json()["id"], res_t.json()["id"]

def test_create_setting_exito(client: TestClient):
    user_id, theme_id = setup_entorno(client)

    response = client.post("/settings/", json={
        "accent_color": "#FF5733",
        "lenguaje": "es",
        "user_id": user_id,
        "theme_id": theme_id
    })
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "es"

def test_get_user_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)
    client.post("/settings/", json={"user_id": user_id, "theme_id": theme_id, "lenguaje": "en"})

    response = client.get(f"/settings/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "en"

def test_update_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)
    res_create = client.post("/settings/", json={"user_id": user_id, "theme_id": theme_id, "lenguaje": "es"})
    setting_id = res_create.json()["id"]

    res_update = client.put(f"/settings/{setting_id}", json={"lenguaje": "fr", "accent_color": "#000000"})
    assert res_update.status_code == 200
    assert res_update.json()["lenguaje"] == "fr"
    assert res_update.json()["accent_color"] == "#000000"

def test_delete_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)
    res_create = client.post("/settings/", json={"user_id": user_id, "theme_id": theme_id})
    setting_id = res_create.json()["id"]

    res_delete = client.delete(f"/settings/{setting_id}")
    assert res_delete.status_code == 200