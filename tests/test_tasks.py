from fastapi.testclient import TestClient
import time

# --- FUNCIÓN DE APOYO ---
# Nos ahorra escribir lo mismo en cada test. Crea un usuario rápido con
# un correo inventado usando la hora actual para no tener fallos de duplicados.
def crear_usuario_helper(client: TestClient):
    timestamp = time.time()
    unique_email = f"task_{timestamp}@test.com"
    res = client.post("/users/", json={
        "user_name": "TaskUser",
        "email": unique_email,
        "password": "123"
    })
    data = res.json()

    # Pillamos el ID devuelto, sea cual sea el nombre del campo de la base de datos.
    return data.get("id") or data.get("_id")


# --- TEST 1: Comprobamos que podemos crear una tarea desde cero ---
def test_create_task_exito(client: TestClient):
    # Genero mi usuario de prueba.
    user_id = crear_usuario_helper(client)

    # Verifico que no se haya roto la creación del usuario antes de meterle la tarea.
    assert user_id is not None

    # Mando los datos para crear la tarea vinculada a ese usuario (¡aprobar el TFG!).
    response = client.post("/tasks/", json={
        "title": "Aprobar el TFG",
        "description": "Hacer los tests",
        "start_date": "2026-05-01T08:00:00",
        "completed": False,
        "user_id": user_id
    })

    # Compruebo que la respuesta de la API es un éxito (200) y que el título está correcto.
    assert response.status_code == 200
    assert response.json()["title"] == "Aprobar el TFG"


# --- TEST 2: Consultar todas las tareas de un usuario en concreto ---
def test_get_user_tasks(client: TestClient):
    user_id = crear_usuario_helper(client)

    # Le asignamos una primera tarea de prueba al usuario que acabamos de crear.
    client.post("/tasks/", json={
        "title": "Tarea 1",
        "start_date": "2026-05-01T08:00:00",
        "description": "Prueba",
        "user_id": user_id
    })

    # Le pedimos a la API que nos traiga todo lo que tenga este usuario.
    response = client.get(f"/tasks/user/{user_id}")
    assert response.status_code == 200

    # Nos aseguramos de que el formato sea una lista y que al menos venga la tarea que le metimos antes.
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


# --- TEST 3: Modificar una tarea existente ---
def test_update_task(client: TestClient):
    user_id = crear_usuario_helper(client)

    # Creamos la tarea original...
    res_create = client.post("/tasks/", json={
        "title": "Tarea Vieja",
        "start_date": "2026-05-01T08:00:00",
        "user_id": user_id
    })

    # ...y nos guardamos su ID para saber a cuál hacerle los cambios.
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mandamos los datos actualizados (cambiamos el título y la marcamos como completada).
    res_update = client.put(f"/tasks/{task_id}", json={
        "title": "Tarea Nueva",
        "completed": True
    })
    assert res_update.status_code == 200

    # Comprobamos en la respuesta que efectivamente se haya quedado guardado el cambio.
    res_data = res_update.json()
    assert res_data["title"] in ["Nueva", "Tarea Nueva"]
    assert res_data["completed"] is True


# --- TEST 4: Borrar una tarea ---
def test_delete_task(client: TestClient):
    user_id = crear_usuario_helper(client)

    # Creamos la típica tarea de prueba que solo existe para ser destruida.
    res_create = client.post("/tasks/", json={
        "title": "Borrar",
        "start_date": "2026-05-01T08:00:00",
        "user_id": user_id
    })
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # Le mandamos a la API la orden de borrado.
    res_delete = client.delete(f"/tasks/{task_id}")

    # Si devuelve el código de OK, todo ha ido bien.
    assert res_delete.status_code == 200