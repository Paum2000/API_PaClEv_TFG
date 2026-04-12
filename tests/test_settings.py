from fastapi.testclient import TestClient
import time

# --- FUNCIÓN DE APOYO ---
# Como el fixture de Pytest ya nos da un usuario normal listo para usar,
# aquí solo necesitamos crear un Tema.
# IMPORTANTE: Pasamos las cabeceras de ADMIN porque un usuario normal no puede crear temas.
def crear_tema_helper(client: TestClient, admin_headers: dict):
    timestamp = time.time()
    res_t = client.post(
        "/themes/",
        json={"name": f"Tema_{timestamp}"},
        headers=admin_headers # Usamos el superpoder aquí
    )

    data_t = res_t.json()
    t_id = data_t.get("id") or data_t.get("_id")
    assert t_id is not None, "Error: El tema no devolvió un ID"

    return t_id


# --- TEST 1: Crear una configuración ---
def test_create_setting_exito(client: TestClient, normal_user_token_headers, admin_token_headers):
    # 1. El Admin crea un tema disponible en el sistema.
    theme_id = crear_tema_helper(client, admin_token_headers)

    # 2. El Usuario Normal crea su configuración.
    # Ya no enviamos "user_id" porque la API lo lee del token.
    response = client.post(
        "/settings/",
        json={
            "lenguaje": "en",
            "accent_color": "#FF5733",
            "theme_id": theme_id
        },
        headers=normal_user_token_headers # Usamos nuestro token normal
    )

    # Compruebo que la API me da luz verde (200) y que guardó el idioma correctamente.
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "en"


# --- TEST 2: Consultar la configuración de un usuario ---
def test_get_mi_configuracion(client: TestClient, normal_user_token_headers, admin_token_headers):
    # 1. Admin crea tema
    theme_id = crear_tema_helper(client, admin_token_headers)

    # 2. Usuario crea su configuración
    client.post(
        "/settings/",
        json={
            "theme_id": theme_id,
            "lenguaje": "es"
        },
        headers=normal_user_token_headers
    )

    # 3. Le pido a la API que me traiga MI configuración (usando la ruta limpia)
    response = client.get("/settings/my_settings", headers=normal_user_token_headers)

    # Verifico que la encuentra (200) y que me trae el idioma que le puse ("es").
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

    # ...y me guardo su ID para saber qué voy a editar.
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mando los nuevos datos (cambio a francés y color negro).
    res_update = client.put(
        f"/settings/{setting_id}",
        json={
            "lenguaje": "fr",
            "accent_color": "#000000"
        },
        headers=normal_user_token_headers
    )

    # Confirmo que no hay errores y que los cambios se aplicaron bien en la respuesta.
    assert res_update.status_code == 200
    assert res_update.json()["lenguaje"] == "fr"
    assert res_update.json()["accent_color"] == "#000000"


# --- TEST 4: Borrar una configuración ---
def test_delete_setting(client: TestClient, normal_user_token_headers, admin_token_headers):
    theme_id = crear_tema_helper(client, admin_token_headers)

    # Creo la configuración
    res_create = client.post(
        "/settings/",
        json={"theme_id": theme_id},
        headers=normal_user_token_headers
    )
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    # Doy la orden de borrarla usando mi token.
    res_delete = client.delete(f"/settings/{setting_id}", headers=normal_user_token_headers)

    # Con el 200 me basta para saber que se fue al hoyo sin problemas.
    assert res_delete.status_code == 200