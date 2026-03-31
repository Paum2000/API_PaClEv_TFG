from fastapi.testclient import TestClient
import time

# --- FUNCIÓN DE APOYO ---
# Prepara el terreno creando un usuario y un tema de "usar y tirar" para que los tests tengan datos con los que jugar.
def setup_entorno(client: TestClient):
    # Uso la hora exacta para inventar nombres y correos distintos cada vez que ejecuto el test.
    timestamp = time.time()
    res_u = client.post("/users/", json={
        "user_name": f"SetUser_{timestamp}",
        "email": f"set_{timestamp}@test.com",
        "password": "123"
    })
    res_t = client.post("/themes/", json={"name": f"Tema_{timestamp}"})

    # TRUCO: Capturo los datos de la respuesta para sacar los IDs.
    data_u = res_u.json()
    data_t = res_t.json()

    # Busco tanto "id" como "_id" por si la base de datos se pone quisquillosa con el nombre del campo.
    u_id = data_u.get("id") or data_u.get("_id")
    t_id = data_t.get("id") or data_t.get("_id")

    # Si por lo que sea no se crean bien, el test corta aquí y me avisa de dónde está el fallo real.
    assert u_id is not None, "Error: El usuario no devolvió un ID"
    assert t_id is not None, "Error: El tema no devolvió un ID"

    # Devuelvo ambos IDs listos para usar en los tests.
    return u_id, t_id


# --- TEST 1: Crear una configuración ---
def test_create_setting_exito(client: TestClient):
    # Traigo mis IDs de prueba.
    user_id, theme_id = setup_entorno(client)

    # Intento crear una configuración uniendo el usuario con el tema.
    response = client.post("/settings/", json={
        "lenguaje": "en",
        "accent_color": "#FF5733",
        "user_id": user_id,
        "theme_id": theme_id
    })

    # Compruebo que la API me da luz verde (200) y que guardó el idioma correctamente.
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "en"


# --- TEST 2: Consultar la configuración de un usuario ---
def test_get_user_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)

    # Primero creo una configuración "a mano" en la BD para asegurarme de que hay algo que consultar.
    client.post("/settings/", json={
        "user_id": user_id,
        "theme_id": theme_id,
        "lenguaje": "es"
    })

    # Ahora sí, le pido a la API que me traiga la configuración de ese usuario.
    response = client.get(f"/settings/user/{user_id}")

    # Verifico que la encuentra (200) y que me trae el idioma que le puse ("es").
    assert response.status_code == 200
    assert response.json()["lenguaje"] == "es"


# --- TEST 3: Editar una configuración ---
def test_update_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)

    # Creo la configuración inicial...
    res_create = client.post("/settings/", json={
        "user_id": user_id,
        "theme_id": theme_id,
        "lenguaje": "es"
    })

    # ...y me guardo su ID para saber qué voy a editar.
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mando los nuevos datos (cambio a francés y color negro).
    res_update = client.put(f"/settings/{setting_id}", json={
        "lenguaje": "fr",
        "accent_color": "#000000"
    })

    # Confirmo que no hay errores y que los cambios se aplicaron bien en la respuesta.
    assert res_update.status_code == 200
    assert res_update.json()["lenguaje"] == "fr"
    assert res_update.json()["accent_color"] == "#000000"


# --- TEST 4: Borrar una configuración ---
def test_delete_setting(client: TestClient):
    user_id, theme_id = setup_entorno(client)

    # Creo la configuración rellenando lo mínimo obligatorio para que no dé un error 422.
    res_create = client.post("/settings/", json={"user_id": user_id, "theme_id": theme_id})
    setting_id = res_create.json().get("id") or res_create.json().get("_id")

    # Doy la orden de borrarla.
    res_delete = client.delete(f"/settings/{setting_id}")

    # Con el 200 me basta para saber que se fue al hoyo sin problemas.
    assert res_delete.status_code == 200