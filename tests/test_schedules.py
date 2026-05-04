from fastapi.testclient import TestClient
import time

# FUNCIONES DE APOYO (HELPERS)
def crear_horario_base_helper(client: TestClient, headers: dict):
    # Crea un horario base y devuelve su ID para usarlo en otros tests.
    timestamp = time.time()
    res = client.post(
        "/schedules/",
        json={"title": f"Horario_{timestamp}"},
        headers=headers
    )
    data = res.json()
    s_id = data.get("id") or data.get("_id")
    assert s_id is not None, "Error: El horario base no devolvió un ID"
    return s_id

def crear_bloque_helper(client: TestClient, headers: dict, schedule_id: int):
    # Crea un bloque dentro de un horario específico y devuelve su ID.
    res = client.post(
        f"/schedules/{schedule_id}/blocks",
        json={
            "title": "Clase de Prueba",
            "weekDay": 1,
            "startHour": "09:00",
            "endHour": "10:00"
        },
        headers=headers
    )
    data = res.json()
    b_id = data.get("id") or data.get("_id")
    assert b_id is not None, "Error: El bloque no devolvió un ID"
    return b_id


# TESTS DEL HORARIO BASE (WeekSchedule)
def test_create_schedule(client: TestClient, normal_user_token_headers):
    # El Usuario Normal crea su propio horario
    response = client.post(
        "/schedules/",
        json={"title": "Mi Horario de Verano"},
        headers=normal_user_token_headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Mi Horario de Verano"


def test_get_mis_horarios(client: TestClient, normal_user_token_headers):
    # 1. Creo un par de horarios para el usuario
    crear_horario_base_helper(client, normal_user_token_headers)
    crear_horario_base_helper(client, normal_user_token_headers)

    # 2. Pido la lista de MIS horarios
    response = client.get("/schedules/", headers=normal_user_token_headers)

    assert response.status_code == 200
    # Verifico que me devuelve una lista y que al menos tiene los que acabo de crear
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2


def test_update_schedule(client: TestClient, normal_user_token_headers):
    # 1. Creo el horario base
    schedule_id = crear_horario_base_helper(client, normal_user_token_headers)

    # 2. Le cambio el nombre
    res_update = client.put(
        f"/schedules/{schedule_id}",
        json={"title": "Horario Definitivo"},
        headers=normal_user_token_headers
    )

    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Horario Definitivo"



# TESTS DE LOS BLOQUES (BlockWeekSchedule)
def test_create_block(client: TestClient, normal_user_token_headers):
    # 1. Necesito un horario donde meter el bloque
    schedule_id = crear_horario_base_helper(client, normal_user_token_headers)

    # 2. Creo el bloque apuntando a ese horario
    response = client.post(
        f"/schedules/{schedule_id}/blocks",
        json={
            "title": "Matemáticas",
            "weekDay": 2,
            "startHour": "10:00",
            "endHour": "11:30",
            "color": "#FF0000"
        },
        headers=normal_user_token_headers
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Matemáticas"
    assert response.json()["week_schedule_id"] == schedule_id


def test_update_block(client: TestClient, normal_user_token_headers):
    # 1. Creo horario y bloque
    schedule_id = crear_horario_base_helper(client, normal_user_token_headers)
    block_id = crear_bloque_helper(client, normal_user_token_headers, schedule_id)

    # 2. Modifico solo el color y la hora del bloque
    res_update = client.put(
        f"/schedules/blocks/{block_id}",
        json={
            "color": "#000000",
            "startHour": "15:00"
        },
        headers=normal_user_token_headers
    )

    assert res_update.status_code == 200
    assert res_update.json()["color"] == "#000000"
    assert res_update.json()["startHour"] == "15:00"
    # El título debería mantenerse intacto
    assert res_update.json()["title"] == "Clase de Prueba"


def test_delete_schedule_en_cascada(client: TestClient, normal_user_token_headers):
    # Comprueba que si borras un horario, te deja borrarlo sin errores.
    schedule_id = crear_horario_base_helper(client, normal_user_token_headers)

    # Le meto un bloque para darle realismo
    crear_bloque_helper(client, normal_user_token_headers, schedule_id)

    # Borro el horario principal
    res_delete = client.delete(f"/schedules/{schedule_id}", headers=normal_user_token_headers)

    # Con el 200 me basta para saber que se borró el horario (y sus bloques en cascada)
    assert res_delete.status_code == 200