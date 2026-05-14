import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_social_coverage(client: TestClient, normal_user_token_headers, other_user_token_headers):
    # --- PREPARACIÓN ---
    res_a = client.get("/users/me", headers=normal_user_token_headers)
    user_a_id = res_a.json().get("id") or res_a.json().get("_id")

    res_b = client.get("/users/me", headers=other_user_token_headers)
    user_b_id = res_b.json().get("id") or res_b.json().get("_id")

    # --- SAD PATHS SOCIALES ---
    # 1. Enviar solicitud a sí mismo (400)
    res = client.post("/friends/request", json={"friend_id": user_a_id}, headers=normal_user_token_headers)
    assert res.status_code == 400

    # 2. Enviar solicitud a un usuario que no existe (400)
    res = client.post("/friends/request", json={"friend_id": 999999}, headers=normal_user_token_headers)
    assert res.status_code == 400

    # --- HAPPY PATH SOCIAL ---
    # 3. Enviar solicitud real (User A -> User B) (200)
    res_req = client.post("/friends/request", json={"friend_id": user_b_id}, headers=normal_user_token_headers)
    assert res_req.status_code == 200
    req_id = res_req.json().get("id") or res_req.json().get("_id")

    # 🚀 NUEVO PASO: Comprobar que aparece como "PENDIENTE" y vienen los datos hidratados
    res_list_pending = client.get("/friends/my_friends", headers=normal_user_token_headers)
    assert res_list_pending.status_code == 200
    pending_data = res_list_pending.json()
    assert len(pending_data) > 0
    # Verificamos la hidratación del Service
    assert pending_data[0]["status"] == "PENDIENTE"
    assert "user_name" in pending_data[0] or "nickname" in pending_data[0]

    # 4. Intentar enviar la misma solicitud otra vez (400)
    res_dup = client.post("/friends/request", json={"friend_id": user_b_id}, headers=normal_user_token_headers)
    assert res_dup.status_code == 400

    # 5. User A intenta aceptar su propia solicitud enviada (400)
    res_bad_acc = client.post(f"/friends/accept/{req_id}", headers=normal_user_token_headers)
    assert res_bad_acc.status_code == 400

    # 6. User B acepta la solicitud de User A (200)
    res_acc = client.post(f"/friends/accept/{req_id}", headers=other_user_token_headers)
    assert res_acc.status_code == 200

    # 7. Listar amigos (Ahora debe salir como ACEPTADO) (200)
    res_list_accepted = client.get("/friends/my_friends", headers=normal_user_token_headers)
    assert res_list_accepted.status_code == 200
    accepted_data = res_list_accepted.json()
    assert len(accepted_data) > 0
    assert accepted_data[0]["status"] == "ACEPTADO"

    # 8. User A elimina a User B de amigos (200)
    res_del = client.delete(f"/friends/{user_b_id}", headers=normal_user_token_headers)
    assert res_del.status_code == 200

    # 9. Intentar eliminar a un amigo que ya no está (404)
    res_del_again = client.delete(f"/friends/{user_b_id}", headers=normal_user_token_headers)
    assert res_del_again.status_code == 404

def test_full_group_coverage(client: TestClient, normal_user_token_headers, other_user_token_headers):
    # --- PREPARACIÓN ---
    res_a = client.get("/users/me", headers=normal_user_token_headers)
    user_a_id = res_a.json().get("id") or res_a.json().get("_id")

    res_b = client.get("/users/me", headers=other_user_token_headers)
    user_b_id = res_b.json().get("id") or res_b.json().get("_id")

    # 1. User A crea un grupo
    res_g = client.post("/groups/", json={"name": "TFG Masters"}, headers=normal_user_token_headers)
    assert res_g.status_code == 200
    g_id = res_g.json().get("id") or res_g.json().get("_id")

    # 🚀 NUEVO: User B (intruso) intenta ver los detalles del grupo (403)
    res_get_bad = client.get(f"/groups/{g_id}", headers=other_user_token_headers)
    assert res_get_bad.status_code == 403

    # 🚀 NUEVO: User B (intruso) intenta ver los miembros del grupo (403)
    res_mem_bad = client.get(f"/groups/{g_id}/members", headers=other_user_token_headers)
    assert res_mem_bad.status_code == 403

    # 3. User B (intruso) intenta cambiar el nombre (403 o 401)
    res_upd_bad = client.put(f"/groups/{g_id}", json={"name": "Hacked Group"}, headers=other_user_token_headers)
    assert res_upd_bad.status_code in [403, 401], f"Esperaba 403, recibí {res_upd_bad.status_code}"

    # 5. User A (Admin) añade a User B
    res_add = client.post(f"/groups/{g_id}/members", json={"user_id": int(user_b_id)}, headers=normal_user_token_headers)
    assert res_add.status_code == 200

    # 6. NUEVO: User B (ahora miembro) ve los detalles del grupo con éxito (200)
    res_get_good = client.get(f"/groups/{g_id}", headers=other_user_token_headers)
    assert res_get_good.status_code == 200

    # 7. NUEVO: User B (ahora miembro) ve la lista de miembros con éxito (200)
    res_mem_good = client.get(f"/groups/{g_id}/members", headers=other_user_token_headers)
    assert res_mem_good.status_code == 200
    assert len(res_mem_good.json()) >= 2  # Al menos deben estar User A y User B

    # 9. User A intenta abandonar su propio grupo
    res_admin_leave = client.delete(f"/groups/{g_id}/members/{user_a_id}", headers=normal_user_token_headers)
    assert res_admin_leave.status_code in [200, 400, 403], f"Error inesperado: {res_admin_leave.status_code}"

    # 11. Borrado final por parte del Admin
    res_del = client.delete(f"/groups/{g_id}", headers=normal_user_token_headers)
    assert res_del.status_code == 200