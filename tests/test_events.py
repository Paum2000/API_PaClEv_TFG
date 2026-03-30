from fastapi.testclient import TestClient
import time

def crear_usuario_helper(client: TestClient):
    """Crea un usuario único y extrae el ID correctamente"""
    timestamp = time.time()
    res = client.post("/users/", json={
        "user_name": "EventUser",
        "email": f"event_{timestamp}@test.com",
        "password": "123"
    })
    # IMPORTANTE: Intentamos capturar ambos nombres por si acaso
    data = res.json()
    return data.get("id") or data.get("_id")

def test_create_event_exito(client: TestClient):
    user_id = crear_usuario_helper(client)

    # Verificamos que el user_id no sea None antes de seguir
    assert user_id is not None

    response = client.post("/events/", json={
        "title": "Reunión Tribunal TFG",
        "description": "Defensa final",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Reunión Tribunal TFG"

def test_get_user_events(client: TestClient):
    user_id = crear_usuario_helper(client)
    client.post("/events/", json={
        "title": "Cena",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })

    response = client.get(f"/events/user/{user_id}")
    assert response.status_code == 200
    # Al ser una lista, comprobamos que llega contenido
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_event(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/events/", json={
        "title": "Fiesta",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    res_update = client.put(f"/events/{event_id}", json={
        "title": "Fiesta Cancelada",
        "description": "No habrá fiesta al final"
    })
    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Fiesta Cancelada"

def test_delete_event(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/events/", json={
        "title": "Borrar",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    # Borramos el evento
    res_delete = client.delete(f"/events/{event_id}")
    assert res_delete.status_code == 200
