from fastapi.testclient import TestClient

# --- TEST 1: Comprobamos que podemos crear un evento sin problemas ---
def test_create_event_exito(client: TestClient, normal_user_token_headers):
    # Fíjate que le pasamos normal_user_token_headers como parámetro.
    # Ya no enviamos "user_id" en el JSON, pero SÍ mandamos las cabeceras.
    response = client.post(
        "/events/",
        json={
            "title": "Reunión Tribunal TFG",
            "description": "Defensa final",
            "start_datetime": "2026-07-01T10:00:00",
            "end_datetime": "2026-07-01T12:00:00"
        },
        headers=normal_user_token_headers
    )

    # Verificamos que la API nos dice que todo ha ido bien (código 200) y que el título coincide.
    assert response.status_code == 200
    assert response.json()["title"] == "Reunión Tribunal TFG"

# --- TEST 2: Comprobamos que podemos listar los eventos de un usuario ---
def test_get_user_events(client: TestClient, normal_user_token_headers):
    # Primero creamos un evento asociado a nuestro token ("Cena").
    client.post(
        "/events/",
        json={
            "title": "Cena",
            "start_datetime": "2026-07-01T10:00:00",
            "end_datetime": "2026-07-01T12:00:00"
        },
        headers=normal_user_token_headers
    )

    # Le pedimos a la API que nos traiga NUESTROS eventos usando la ruta limpia.
    response = client.get("/events/my_events", headers=normal_user_token_headers)

    assert response.status_code == 200

    # Comprobamos que efectivamente nos devuelve una lista y que tiene al menos el evento.
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

# --- TEST 3: Comprobamos que podemos actualizar/editar un evento ---
def test_update_event(client: TestClient, normal_user_token_headers):
    # Creamos un evento ("Fiesta") y nos guardamos el ID.
    res_create = client.post(
        "/events/",
        json={
            "title": "Fiesta",
            "start_datetime": "2026-07-01T10:00:00",
            "end_datetime": "2026-07-01T12:00:00"
        },
        headers=normal_user_token_headers
    )
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    # Modificamos el evento usando el método PUT.
    res_update = client.put(
        f"/events/{event_id}",
        json={
            "title": "Fiesta Cancelada",
            "description": "No habrá fiesta al final"
        },
        headers=normal_user_token_headers
    )

    # Revisamos que no haya dado error y que el título se haya actualizado correctamente.
    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Fiesta Cancelada"

# --- TEST 4: Comprobamos que podemos borrar un evento ---
def test_delete_event(client: TestClient, normal_user_token_headers):
    # Lo de siempre: preparamos el terreno creando un evento.
    res_create = client.post(
        "/events/",
        json={
            "title": "Borrar",
            "start_datetime": "2026-07-01T10:00:00",
            "end_datetime": "2026-07-01T12:00:00"
        },
        headers=normal_user_token_headers
    )
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mandamos la orden de borrar ese evento en concreto usando nuestro token.
    res_delete = client.delete(f"/events/{event_id}", headers=normal_user_token_headers)

    # Con que nos devuelva un 200 (OK), sabemos que se ha borrado bien.
    assert res_delete.status_code == 200