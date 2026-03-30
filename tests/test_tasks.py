from fastapi.testclient import TestClient
import time

def crear_usuario_helper(client: TestClient):
    """Crea un usuario con email único y extrae su ID correctamente"""
    timestamp = time.time()
    unique_email = f"task_{timestamp}@test.com"
    res = client.post("/users/", json={
        "user_name": "TaskUser",
        "email": unique_email,
        "password": "123"
    })
    data = res.json()
    # Capturamos id o _id para evitar el None
    return data.get("id") or data.get("_id")

def test_create_task_exito(client: TestClient):
    user_id = crear_usuario_helper(client)

    # Aseguramos que el usuario se creó bien antes de seguir
    assert user_id is not None

    response = client.post("/tasks/", json={
        "title": "Aprobar el TFG",
        "description": "Hacer los tests",
        "start_date": "2026-05-01T08:00:00",
        "completed": False,
        "user_id": user_id
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Aprobar el TFG"

def test_get_user_tasks(client: TestClient):
    user_id = crear_usuario_helper(client)

    # Creamos una tarea vinculada al usuario
    client.post("/tasks/", json={
        "title": "Tarea 1",
        "start_date": "2026-05-01T08:00:00",
        "description": "Prueba",
        "user_id": user_id
    })

    # Ruta de la API: /tasks/user/{user_id}
    response = client.get(f"/tasks/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_task(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/tasks/", json={
        "title": "Tarea Vieja",
        "start_date": "2026-05-01T08:00:00", # <--- ¡Añadido!
        "user_id": user_id
    })

    # Captura dinámica de ID de la tarea
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    res_update = client.put(f"/tasks/{task_id}", json={
        "title": "Tarea Nueva",
        "completed": True
    })
    assert res_update.status_code == 200

    res_data = res_update.json()
    assert res_data["title"] in ["Nueva", "Tarea Nueva"]
    assert res_data["completed"] is True

def test_delete_task(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/tasks/", json={
        "title": "Borrar",
        "start_date": "2026-05-01T08:00:00",
        "user_id": user_id
    })
    task_id = res_create.json().get("id") or res_create.json().get("_id")

    # Borramos la tarea
    res_delete = client.delete(f"/tasks/{task_id}")
    assert res_delete.status_code == 200
