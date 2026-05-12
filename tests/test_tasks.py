from fastapi.testclient import TestClient

# --- TEST 1: Comprobamos que podemos crear una tarea desde cero ---
def test_create_task_exito(client: TestClient, normal_user_token_headers):
    # Mando los datos para crear la tarea (¡aprobar el TFG!).
    # Fíjate que ya NO mandamos el user_id, pero SÍ el token de seguridad.
    response = client.post(
        "/tasks/",
        json={
            "title": "Aprobar el TFG",
            "description": "Hacer los tests",
            "start_date": "2026-05-01T08:00:00",
            "completed": False
        },
        headers=normal_user_token_headers # Nuestra llave
    )

    # Compruebo que la respuesta de la API es un éxito (200) y que el título está correcto.
    assert response.status_code == 200
    assert response.json()["title"] == "Aprobar el TFG"


# --- TEST 2: Consultar todas las tareas de un usuario en concreto ---
def test_get_user_tasks(client: TestClient, normal_user_token_headers):
    # Le asignamos una primera tarea de prueba al usuario actual.
    client.post(
        "/tasks/",
        json={
            "title": "Tarea 1",
            "start_date": "2026-05-01T08:00:00",
            "description": "Prueba"
        },
        headers=normal_user_token_headers
    )

    # Le pedimos a la API que nos traiga nuestras tareas usando la ruta nueva.
    response = client.get("/tasks/my_tasks", headers=normal_user_token_headers)
    assert response.status_code == 200

    # Nos aseguramos de que el formato sea una lista y que al menos venga la tarea que le metimos antes.
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


# --- TEST 3: Modificar una tarea existente ---
def test_update_task(client: TestClient, normal_user_token_headers):
    # Creamos la tarea original...
    res_create = client.post(
        "/tasks/",
        json={
            "title": "Tarea Vieja",
            "start_date": "2026-05-01T08:00:00"
        },
        headers=normal_user_token_headers
    )

    # ...y nos guardamos su ID para saber a cuál hacerle los cambios.
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mandamos los datos actualizados (cambiamos el título y la marcamos como completada).
    res_update = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Tarea Nueva",
            "completed": True
        },
        headers=normal_user_token_headers
    )
    assert res_update.status_code == 200

    # Comprobamos en la respuesta que efectivamente se haya quedado guardado el cambio.
    res_data = res_update.json()
    assert res_data["title"] in ["Nueva", "Tarea Nueva"]
    assert res_data["completed"] is True


# --- TEST 4: Borrar una tarea ---
def test_delete_task(client: TestClient, normal_user_token_headers):
    # Creamos la típica tarea de prueba que solo existe para ser destruida.
    res_create = client.post(
        "/tasks/",
        json={
            "title": "Borrar",
            "start_date": "2026-05-01T08:00:00"
        },
        headers=normal_user_token_headers
    )
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # Le mandamos a la API la orden de borrado validando nuestra identidad.
    res_delete = client.delete(f"/tasks/{task_id}", headers=normal_user_token_headers)

    # Si devuelve el código de OK, todo ha ido bien.
    assert res_delete.status_code == 200


# --- TEST 5: Completar una tarea otorga puntos (Gamificación) ---
def test_completar_tarea_da_puntos(client: TestClient, normal_user_token_headers):
    # 1. Creamos una tarea nueva sin completar
    res_create = client.post(
        "/tasks/",
        json={
            "title": "Tarea para ganar puntos",
            "start_date": "2026-05-01T08:00:00",
            "completed": False
        },
        headers=normal_user_token_headers
    )
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # 2. Consultamos a la API cuántos puntos tenemos ANTES de completarla
    res_me_antes = client.get("/users/me", headers=normal_user_token_headers)
    puntos_antes = res_me_antes.json().get("points", 0)

    # 3. Marcamos la tarea como completada (esto debe disparar la lógica interna de la API)
    client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=normal_user_token_headers
    )

    # 4. Volvemos a consultar nuestros puntos DESPUÉS de completarla
    res_me_despues = client.get("/users/me", headers=normal_user_token_headers)
    puntos_despues = res_me_despues.json().get("points", 0)

    # 5. Comprobamos que la magia del TFG ha funcionado: nos han sumado 10 puntos.
    assert puntos_despues == puntos_antes + 10


# --- TEST 6: 🚀 NUEVO - Flujo Colaborativo y Seguridad para Tareas ---
def test_group_tasks_flow(client: TestClient, normal_user_token_headers, other_user_token_headers):
    # 1. El usuario A crea un grupo (ej: Equipo TFG)
    res_group = client.post("/groups/", json={"name": "Equipo TFG"}, headers=normal_user_token_headers)
    assert res_group.status_code == 200
    group_id = res_group.json().get("id") or res_group.json().get("_id")

    # 2. El usuario A crea una tarea y la asigna al grupo
    res_task = client.post(
        "/tasks/",
        json={
            "title": "Redactar la memoria",
            "start_date": "2026-05-15T09:00:00",
            "group_id": group_id
        },
        headers=normal_user_token_headers
    )
    assert res_task.status_code == 200
    assert res_task.json()["group_id"] == group_id

    # 3. Happy Path: El usuario A pide las tareas de su grupo
    res_get_group = client.get(f"/tasks/group/{group_id}", headers=normal_user_token_headers)
    assert res_get_group.status_code == 200
    data = res_get_group.json()
    assert len(data) >= 1
    assert any(t["title"] == "Redactar la memoria" for t in data)

    # 4. Sad Path (Seguridad): El usuario B intenta espiar las tareas del grupo de A
    res_forbidden = client.get(f"/tasks/group/{group_id}", headers=other_user_token_headers)
    assert res_forbidden.status_code == 403
    assert "permiso" in res_forbidden.json()["detail"].lower()