from fastapi.testclient import TestClient

def crear_usuario_helper(client: TestClient):
    res = client.post("/users/", json={"user_name": "EventUser", "email": "event@test.com", "password": "123"})
    return res.json()["id"]

def test_create_event_exito(client: TestClient):
    user_id = crear_usuario_helper(client)

    response = client.post("/events/", json={
        "title": "Reunión Tribunal TFG",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "is_all_day": False,
        "user_id": user_id
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Reunión Tribunal TFG"

def test_get_user_events(client: TestClient):
    user_id = crear_usuario_helper(client)
    client.post("/events/", json={
        "title": "Cena", "start_datetime": "2026-01-01T20:00:00", "end_datetime": "2026-01-01T22:00:00", "user_id": user_id
    })

    response = client.get(f"/events/user/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_update_event(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/events/", json={
        "title": "Fiesta", "start_datetime": "2026-01-01T20:00:00", "end_datetime": "2026-01-01T22:00:00", "user_id": user_id
    })
    event_id = res_create.json()["id"]

    res_update = client.put(f"/events/{event_id}", json={"is_all_day": True, "title": "Fiesta Cancelada"})
    assert res_update.status_code == 200
    assert res_update.json()["is_all_day"] == True

def test_delete_event(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/events/", json={
        "title": "Borrar", "start_datetime": "2026-01-01T20:00:00", "end_datetime": "2026-01-01T22:00:00", "user_id": user_id
    })
    event_id = res_create.json()["id"]

    res_delete = client.delete(f"/events/{event_id}")
    assert res_delete.status_code == 200