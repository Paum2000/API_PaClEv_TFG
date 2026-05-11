from fastapi.testclient import TestClient
import time

# --- FUNCIÓN DE APOYO ---
def crear_tema_helper(client: TestClient, admin_headers: dict):
    timestamp = time.time()
    res_t = client.post(
        "/themes/",
        # 💡 CAMBIO: Lo hacemos gratuito y por defecto para saltar el candado
        json={"name": f"Tema_{timestamp}", "price": 0, "is_default": True},
        headers=admin_headers
    )

    data_t = res_t.json()
    t_id = data_t.get("id") or data_t.get("_id")
    assert t_id is not None, "Error: El tema no devolvió un ID"

    return t_id


# --- TEST 1: Crear una configuración ---
def test_create_setting_exito(client: TestClient, normal_user_token_headers, admin_token_headers):
    # 1. El Admin crea un tema gratuito.
    theme_id = crear_tema_helper(client, admin_token_headers)

    # 2. El Usuario Normal crea su configuración.
    response = client.post(
        "/settings/",
        json={
            "lenguaje": "en",
            "theme_id": theme_id
            # 💡 CAMBIO: Omitimos accent_color para usar el 'null' gratuito
        },
        headers=normal_user_token_headers
    )

    assert response.status_code == 200
    assert response.json()["lenguaje"] == "en"


# --- TEST 2: Consultar la configuración de un usuario ---
def test_get_mi_configuracion(client: TestClient, normal_user_token_headers, admin_token_headers):
    theme_id = crear_tema_helper(client, admin_token_headers)

    client.post(
        "/settings/",
        json={
            "theme_id": theme_id,
            "lenguaje": "es"
        },
        headers=normal_user_token_headers
    )

    response = client.get("/settings/my_settings", headers=normal_user_token_headers)

    assert response.status_code == 200
    assert response.json()["lenguaje"] == "es"


# --- TEST 3: Editar una configuración ---
def test_update_setting(client: TestClient, normal_user_token_headers, admin_token_headers):
    theme_id = crear_tema_helper(client, admin_token_headers)

    # Creo la configuración inicial...
    res_create = client.post(
        "/settings/",
        json={
            "theme_id": theme_id,
            "lenguaje": "es"
        },
        headers=normal_user_token_headers
    )

    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mando los nuevos datos
    res_update = client.put(
        f"/settings/{setting_id}",
        json={
            "lenguaje": "fr"
            # 💡 CAMBIO: Quitamos el accent_color de pago
        },
        headers=normal_user_token_headers
    )

    assert res_update.status_code == 200
    assert res_update.json()["lenguaje"] == "fr"


# --- TEST 4: Borrar una configuración ---
def test_delete_setting(client: TestClient, normal_user_token_headers, admin_token_headers):
    theme_id = crear_tema_helper(client, admin_token_headers)

    res_create = client.post(
        "/settings/",
        json={"theme_id": theme_id},
        headers=normal_user_token_headers
    )
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    res_delete = client.delete(f"/settings/{setting_id}", headers=normal_user_token_headers)

    assert res_delete.status_code == 200