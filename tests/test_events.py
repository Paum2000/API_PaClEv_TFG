from fastapi.testclient import TestClient

# --- TEST 1: Comprobamos que podemos crear un evento sin problemas ---
def test_create_event_exito(client: TestClient, normal_user_token_headers):
    response = client.post(
        "/events/",
        json={
            "title": "Reunión Tribunal TFG",
            "description": "Defensa final",
            "start_date": "2026-07-01",        
            "start_time": "10:00:00",
            "end_date": "2026-07-01",
            "end_time": "12:00:00",
            "color": "#FF0000"
        },
        headers=normal_user_token_headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Reunión Tribunal TFG"

# --- TEST 2: Comprobamos que podemos listar los eventos de un usuario ---
def test_get_user_events(client: TestClient, normal_user_token_headers):
    client.post(
        "/events/",
        json={
            "title": "Cena",
            "start_date": "2026-07-01",
            "start_time": "21:00:00"
        },
        headers=normal_user_token_headers
    )

    response = client.get("/events/my_events", headers=normal_user_token_headers)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

# --- TEST 3: Comprobamos que podemos actualizar/editar un evento ---
def test_update_event(client: TestClient, normal_user_token_headers):
    res_create = client.post(
        "/events/",
        json={
            "title": "Fiesta",
            "start_date": "2026-07-01",
            "start_time": "22:00:00"
        },
        headers=normal_user_token_headers
    )
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    res_update = client.put(
        f"/events/{event_id}",
        json={
            "title": "Fiesta Cancelada",
            "description": "No habrá fiesta al final",
            "is_all_day": True                 # Probamos uno de tus nuevos booleanos
        },
        headers=normal_user_token_headers
    )

    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Fiesta Cancelada"

# --- TEST 4: Comprobamos que podemos borrar un evento ---
def test_delete_event(client: TestClient, normal_user_token_headers):
    res_create = client.post(
        "/events/",
        json={
            "title": "Borrar",
            "start_date": "2026-07-01",
        },
        headers=normal_user_token_headers
    )
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    res_delete = client.delete(f"/events/{event_id}", headers=normal_user_token_headers)

    assert res_delete.status_code == 200