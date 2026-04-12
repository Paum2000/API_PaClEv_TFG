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