from fastapi.testclient import TestClient
import time

# Función de apoyo para no repetir código en todos los tests.
# Nos crea un usuario rápido de "usar y tirar" y nos devuelve su ID.
def crear_usuario_helper(client: TestClient):
    # Usamos la hora actual para inventarnos un email distinto cada vez y que no de error por duplicado.
    timestamp = time.time()
    res = client.post("/users/", json={
        "user_name": "EventUser",
        "email": f"event_{timestamp}@test.com",
        "password": "123"
    })

    # Intentamos capturar el ID sea como sea ("id" o "_id") según lo devuelva nuestra base de datos.
    data = res.json()
    return data.get("id") or data.get("_id")

# --- TEST 1: Comprobamos que podemos crear un evento sin problemas ---
def test_create_event_exito(client: TestClient):
    # Pedimos un usuario de prueba a nuestra función de apoyo.
    user_id = crear_usuario_helper(client)

    # Nos aseguramos de que el usuario se ha creado bien y tenemos su ID antes de seguir.
    assert user_id is not None

    # Intentamos crear el evento asociado a ese usuario.
    response = client.post("/events/", json={
        "title": "Reunión Tribunal TFG",
        "description": "Defensa final",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })

    # Verificamos que la API nos dice que todo ha ido bien (código 200) y que el título coincide.
    assert response.status_code == 200
    assert response.json()["title"] == "Reunión Tribunal TFG"

# --- TEST 2: Comprobamos que podemos listar los eventos de un usuario ---
def test_get_user_events(client: TestClient):
    # Creamos usuario y le metemos un evento ("Cena").
    user_id = crear_usuario_helper(client)
    client.post("/events/", json={
        "title": "Cena",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })

    # Le pedimos a la API que nos traiga los eventos de este usuario.
    response = client.get(f"/events/user/{user_id}")
    assert response.status_code == 200

    # Comprobamos que efectivamente nos devuelve una lista y que tiene al menos el evento de la cena.
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

# --- TEST 3: Comprobamos que podemos actualizar/editar un evento ---
def test_update_event(client: TestClient):
    # Creamos el usuario, luego un evento ("Fiesta") y nos guardamos el ID del evento.
    user_id = crear_usuario_helper(client)
    res_create = client.post("/events/", json={
        "title": "Fiesta",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    # Modificamos el evento usando el método PUT.
    res_update = client.put(f"/events/{event_id}", json={
        "title": "Fiesta Cancelada",
        "description": "No habrá fiesta al final"
    })

    # Revisamos que no haya dado error y que el título se haya actualizado correctamente.
    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Fiesta Cancelada"

# --- TEST 4: Comprobamos que podemos borrar un evento ---
def test_delete_event(client: TestClient):
    # Lo de siempre: preparamos el terreno creando usuario y evento.
    user_id = crear_usuario_helper(client)
    res_create = client.post("/events/", json={
        "title": "Borrar",
        "start_datetime": "2026-07-01T10:00:00",
        "end_datetime": "2026-07-01T12:00:00",
        "user_id": user_id
    })
    event_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mandamos la orden de borrar ese evento en concreto.
    res_delete = client.delete(f"/events/{event_id}")

    # Con que nos devuelva un 200 (OK), sabemos que se ha borrado bien.
    assert res_delete.status_code == 200