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

    # 4. Intentar enviar la misma solicitud otra vez (400)
    res_dup = client.post("/friends/request", json={"friend_id": user_b_id}, headers=normal_user_token_headers)
    assert res_dup.status_code == 400

    # 5. User A intenta aceptar su propia solicitud enviada (400)
    res_bad_acc = client.post(f"/friends/accept/{req_id}", headers=normal_user_token_headers)
    assert res_bad_acc.status_code == 400

    # 6. User B acepta la solicitud de User A (200)
    res_acc = client.post(f"/friends/accept/{req_id}", headers=other_user_token_headers)
    assert res_acc.status_code == 200

    # 7. Listar amigos (Debe salir 1 amigo) (200)
    res_list = client.get("/friends/my_friends", headers=normal_user_token_headers)
    assert res_list.status_code == 200
    assert len(res_list.json()) > 0

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

    # --- HAPPY PATH GRUPOS ---
    # 1. User A crea un grupo (200)
    res_g = client.post("/groups/", json={"name": "TFG Masters"}, headers=normal_user_token_headers)
    assert res_g.status_code == 200
    g_id = res_g.json().get("id") or res_g.json().get("_id")

    # 2. User A actualiza el nombre del grupo (200)
    res_upd = client.put(f"/groups/{g_id}", json={"name": "TFG Masters Pro"}, headers=normal_user_token_headers)
    assert res_upd.status_code == 200

    # --- SAD PATHS GRUPOS ---
    # 3. User B (intruso) intenta cambiar el nombre del grupo (403)
    res_upd_bad = client.put(f"/groups/{g_id}", json={"name": "Hacked Group"}, headers=other_user_token_headers)
    assert res_upd_bad.status_code == 403

    # 4. User B intenta añadir a un usuario random (400)
    res_add_bad = client.post(f"/groups/{g_id}/members", json={"user_id": 999}, headers=other_user_token_headers)
    assert res_add_bad.status_code == 400

    # --- FLUJO DE MIEMBROS ---
    # 5. User A (Admin) añade a User B (200)
    res_add = client.post(f"/groups/{g_id}/members", json={"user_id": user_b_id}, headers=normal_user_token_headers)
    assert res_add.status_code == 200

    # 6. User A intenta añadir a B OTRA VEZ (400 - Duplicado)
    res_add_dup = client.post(f"/groups/{g_id}/members", json={"user_id": user_b_id}, headers=normal_user_token_headers)
    assert res_add_dup.status_code == 400

    # 7. User B decide abandonar el grupo voluntariamente (200)
    res_leave = client.delete(f"/groups/{g_id}/members/{user_b_id}", headers=other_user_token_headers)
    assert res_leave.status_code == 200

    # 8. User A intenta expulsar a User B que ya se ha ido (400)
    res_exp_bad = client.delete(f"/groups/{g_id}/members/{user_b_id}", headers=normal_user_token_headers)
    assert res_exp_bad.status_code == 400

    # 9. User A (Admin) intenta borrarse a sí mismo y abandonar su propio grupo (400 o 403)
    res_admin_leave = client.delete(f"/groups/{g_id}/members/{user_a_id}", headers=normal_user_token_headers)
    assert res_admin_leave.status_code in [400, 403]

    # 10. User B (intruso) intenta borrar el grupo de A (403)
    res_del_bad = client.delete(f"/groups/{g_id}", headers=other_user_token_headers)
    assert res_del_bad.status_code == 403

    # 11. User A (Admin) borra su propio grupo correctamente (200)
    res_del = client.delete(f"/groups/{g_id}", headers=normal_user_token_headers)
    assert res_del.status_code == 200