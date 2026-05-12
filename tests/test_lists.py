from fastapi.testclient import TestClient

# --- TEST 1: Comprobamos que podemos crear una lista con items ---
def test_create_list_exito(client: TestClient, normal_user_token_headers):
    # Mandamos crear una lista de la compra con un par de strings en el array
    response = client.post(
        "/lists/",
        json={
            "name": "Lista de la compra",
            "items": ["Manzanas", "Leche", "Pan"]
        },
        headers=normal_user_token_headers
    )

    # Verificamos que todo ha ido bien (200) y que nos devuelve los datos correctos
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lista de la compra"
    assert len(data["items"]) == 3
    assert "Leche" in data["items"]

# --- TEST 2: Comprobamos que podemos obtener las listas del usuario ---
def test_get_my_lists(client: TestClient, normal_user_token_headers):
    # Primero creamos una lista vacía de ejemplo
    client.post(
        "/lists/",
        json={
            "name": "Películas por ver",
            # Como 'items' es opcional y por defecto es [], no hace falta enviarlo
        },
        headers=normal_user_token_headers
    )

    # Le pedimos a la API todas mis listas
    response = client.get("/lists/my_lists", headers=normal_user_token_headers)

    assert response.status_code == 200
    data = response.json()

    # Comprobamos que devuelve un array y que al menos tiene la lista que acabamos de crear
    assert isinstance(data, list)
    assert len(data) >= 1

# --- TEST 3: Comprobamos que podemos actualizar una lista (cambiar nombre y añadir items) ---
def test_update_list(client: TestClient, normal_user_token_headers):
    # Creamos una lista base
    res_create = client.post(
        "/lists/",
        json={"name": "Tareas casa", "items": ["Barrer"]},
        headers=normal_user_token_headers
    )
    list_id = res_create.json().get("id") or res_create.json().get("_id")

    # La actualizamos usando el ID numérico
    res_update = client.put(
        f"/lists/{list_id}",
        json={
            "name": "Tareas casa (Urgente)",
            "items": ["Barrer", "Fregar", "Quitar polvo"]
        },
        headers=normal_user_token_headers
    )

    assert res_update.status_code == 200
    data_updated = res_update.json()

    # Comprobamos que se han guardado los cambios
    assert data_updated["name"] == "Tareas casa (Urgente)"
    assert len(data_updated["items"]) == 3

# --- TEST 4: Comprobamos que podemos borrar una lista ---
def test_delete_list(client: TestClient, normal_user_token_headers):
    # Preparamos una lista para sacrificarla
    res_create = client.post(
        "/lists/",
        json={"name": "Lista para borrar"},
        headers=normal_user_token_headers
    )
    list_id = res_create.json().get("id") or res_create.json().get("_id")

    # Mandamos la petición de borrado
    res_delete = client.delete(f"/lists/{list_id}", headers=normal_user_token_headers)

    # Verificamos el OK
    assert res_delete.status_code == 200
    assert res_delete.json()["message"] == "Lista eliminada correctamente"

# --- TEST 5: 🚀 NUEVO - Flujo Colaborativo y Seguridad para Listas ---
def test_group_lists_flow(client: TestClient, normal_user_token_headers, other_user_token_headers):
    # 1. El usuario A crea un grupo (ej: Compañeros de piso)
    res_group = client.post("/groups/", json={"name": "Piso Compartido"}, headers=normal_user_token_headers)
    assert res_group.status_code == 200
    group_id = res_group.json().get("id") or res_group.json().get("_id")

    # 2. El usuario A crea una lista y la asigna al grupo
    res_list = client.post(
        "/lists/",
        json={
            "name": "Compra conjunta",
            "items": ["Friegasuelos", "Papel higiénico"],
            "group_id": group_id
        },
        headers=normal_user_token_headers
    )
    assert res_list.status_code == 200
    assert res_list.json()["group_id"] == group_id

    # 3. Happy Path: El usuario A pide las listas de su grupo
    res_get_group = client.get(f"/lists/group/{group_id}", headers=normal_user_token_headers)
    assert res_get_group.status_code == 200
    data = res_get_group.json()
    assert len(data) >= 1
    assert any(l["name"] == "Compra conjunta" for l in data)

    # 4. Sad Path (Seguridad): El usuario B intenta espiar la lista del grupo de A
    res_forbidden = client.get(f"/lists/group/{group_id}", headers=other_user_token_headers)
    assert res_forbidden.status_code == 403
    assert "permiso" in res_forbidden.json()["detail"].lower()