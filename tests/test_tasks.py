from fastapi.testclient import TestClient

def crear_usuario_helper(client: TestClient):
    """Función de ayuda para crear un usuario y devolver su ID"""
    res = client.post("/users/", json={"user_name": "TaskUser", "email": "task@test.com", "password": "123"})
    return res.json()["id"]

def test_create_task_exito(client: TestClient):
    user_id = crear_usuario_helper(client)

    response = client.post("/tasks/", json={
        "title": "Aprobar el TFG",
        "description": "Hacer los tests",
        "start_date": "2026-05-01T08:00:00",
        "done_date": "2026-06-15T10:00:00",
        "user_id": user_id,
        "priority": "Alta"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Aprobar el TFG"

def test_get_user_tasks(client: TestClient):
    user_id = crear_usuario_helper(client)
    client.post("/tasks/", json={
        "title": "Tarea 1", "start_date": "2026-01-01T00:00:00", "done_date": "2026-01-02T00:00:00", "user_id": user_id
    })

    response = client.get(f"/tasks/user/{user_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_update_task(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/tasks/", json={
        "title": "Vieja", "start_date": "2026-01-01T00:00:00", "done_date": "2026-01-02T00:00:00", "user_id": user_id
    })
    task_id = res_create.json()["id"]

    res_update = client.put(f"/tasks/{task_id}", json={"title": "Nueva", "done": True})
    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Nueva"
    assert res_update.json()["done"] == True

def test_delete_task(client: TestClient):
    user_id = crear_usuario_helper(client)
    res_create = client.post("/tasks/", json={
        "title": "Borrar", "start_date": "2026-01-01T00:00:00", "done_date": "2026-01-02T00:00:00", "user_id": user_id
    })
    task_id = res_create.json()["id"]

    res_delete = client.delete(f"/tasks/{task_id}")
    assert res_delete.status_code == 200