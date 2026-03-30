from fastapi.testclient import TestClient
import time

def setup_entorno(client: TestClient):
    """Crea un usuario y un tema únicos para cada test"""
    timestamp = time.time()
    # Email único para evitar errores de duplicado
    res_u = client.post("/users/", json={
        "user_name": f"SetUser_{timestamp}",
        "email": f"set_{timestamp}@test.com",
        "password": "123"
    })
    res_t = client.post("/themes/", json={"name": f"Tema_{timestamp}"})

    # TRUCO MAESTRO: Capturamos 'id' o '_id' para evitar el None
    data_u = res_u.json()
    data_t = res_t.json()

    u_id = data_u.get("id") or data_u.get("_id")
    t_id = data_t.get("id") or data_t.get("_id")

    # Si estos fallan, sabremos que el error está en la creación del usuario/tema
    assert u_id is not None, "Error: El usuario no devolvió un ID"
    assert t_id is not None, "Error: El tema no devolvió un ID"

    return u_id, t_id

def test_create_setting_exito(client: TestClient):
    user_id, theme_id = setup_entorno(client)

    response = client.post("/settings/", json={
        "lenguaje": "en",
        "accent_color": "#FF5733",
        "user_id": user_id,
        "theme_id": theme_id # <-- ¡Ahora sí lo enviamos!
    })
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "en"

def test_get_user_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)

    # Creamos la configuración inicial en la base de datos
    client.post("/settings/", json={
        "user_id": user_id,
        "theme_id": theme_id,
        "lenguaje": "es"
    })

    # Ahora sí, el GET debe devolver un 200 OK porque la acabamos de crear
    response = client.get(f"/settings/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "es"

def test_update_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)
    res_create = client.post("/settings/", json={
        "user_id": user_id,
        "theme_id": theme_id,
        "lenguaje": "es"
    })

    # Captura dinámica de ID
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    res_update = client.put(f"/settings/{setting_id}", json={
        "lenguaje": "fr",
        "accent_color": "#000000"
    })
    assert res_update.status_code == 200
    assert res_update.json()["lenguaje"] == "fr"
    assert res_update.json()["accent_color"] == "#000000"

def test_delete_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)
    # Incluimos theme_id para que no dé Error 422
    res_create = client.post("/settings/", json={"user_id": user_id, "theme_id": theme_id})
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    res_delete = client.delete(f"/settings/{setting_id}")
    assert res_delete.status_code == 200