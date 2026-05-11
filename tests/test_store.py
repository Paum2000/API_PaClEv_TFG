from fastapi.testclient import TestClient
import time

def crear_tema_premium_helper(client: TestClient, headers: dict):
    """Crea un tema de pago (Premium) para las pruebas."""
    timestamp = time.time()
    res = client.post(
        "/themes/",
        json={"name": f"Premium_{timestamp}", "price": 500, "is_default": False},
        headers=headers
    )
    return res.json().get("id") or res.json().get("_id")

def test_get_inventory(client: TestClient, normal_user_token_headers):
    """Prueba que el inventario carga correctamente (aunque esté vacío de compras)."""
    response = client.get("/store/my-inventory", headers=normal_user_token_headers)

    assert response.status_code == 200
    data = response.json()
    assert "themes" in data
    assert "colors" in data
    # Por defecto, el color negro debería estar disponible o la lista inicializarse
    assert isinstance(data["themes"], list)
    assert isinstance(data["colors"], list)

def test_buy_theme_insufficient_points(client: TestClient, normal_user_token_headers, admin_token_headers):
    """Prueba que un usuario sin puntos no pueda comprar un tema premium."""
    # 1. El admin crea un tema premium de 500 puntos
    theme_id = crear_tema_premium_helper(client, admin_token_headers)

    # 2. El usuario (que acaba de registrarse y tiene 0 puntos) intenta comprarlo
    response = client.post(
        f"/store/buy-theme/{theme_id}",
        headers=normal_user_token_headers
    )

    # 3. Verificamos que el servidor lo rechaza con un 400
    assert response.status_code == 400
    assert "Puntos insuficientes" in response.json()["detail"]

def test_buy_color_insufficient_points(client: TestClient, normal_user_token_headers):
    """Prueba que un usuario sin puntos no pueda comprar un color."""
    response = client.post(
        "/store/buy-color",
        json={"hex_color": "#FF00FF"},
        headers=normal_user_token_headers
    )

    assert response.status_code == 400
    assert "Puntos insuficientes" in response.json()["detail"]

def test_buy_default_theme_error(client: TestClient, normal_user_token_headers, admin_token_headers):
    """Prueba que no se pueda comprar un tema que ya es gratis."""
    # 1. Admin crea tema gratuito por defecto
    timestamp = time.time()
    res_t = client.post(
        "/themes/",
        json={"name": f"Gratis_{timestamp}", "price": 0, "is_default": True},
        headers=admin_token_headers
    )
    theme_id = res_t.json().get("id") or res_t.json().get("_id")

    # 2. El usuario intenta comprarlo
    response = client.post(
        f"/store/buy-theme/{theme_id}",
        headers=normal_user_token_headers
    )

    # 3. Rechazado porque ya lo tiene gratis
    assert response.status_code == 400
    assert "desbloqueado por defecto" in response.json()["detail"]

# --- TEST 6: Comprar un tema con ÉXITO ---
def test_buy_theme_success(client: TestClient, normal_user_token_headers, admin_token_headers):
    # 1. El Admin crea un tema barato (10 puntos)
    timestamp = time.time()
    res_t = client.post(
        "/themes/",
        json={"name": f"Barato_{timestamp}", "price": 10, "is_default": False},
        headers=admin_token_headers
    )
    theme_id = res_t.json().get("id") or res_t.json().get("_id")

    # 2. El usuario completa una tarea para ganar 10 puntos
    res_task = client.post(
        "/tasks/",
        json={"title": "Ganar puntos", "start_date": "2026-05-11", "completed": False},
        headers=normal_user_token_headers
    )
    task_id = res_task.json().get("id") or res_task.json().get("_id")
    client.put(f"/tasks/{task_id}", json={"completed": True}, headers=normal_user_token_headers)

    # 3. COMPRA
    response = client.post(f"/store/buy-theme/{theme_id}", headers=normal_user_token_headers)

    # 4. VERIFICACIÓN (Ajustamos el mensaje exacto del service)
    assert response.status_code == 200
    assert "comprado con éxito" in response.json()["message"] # 💡 Mensaje corregido


# --- TEST 7: Comprar un color con ÉXITO ---
def test_buy_color_success(client: TestClient, normal_user_token_headers):
    # 1. El usuario completa 10 tareas para ganar los 100 puntos del día
    for i in range(10):
        res_task = client.post("/tasks/",
                               json={"title": f"Tarea puntos {i}", "start_date": "2026-05-11"},
                               headers=normal_user_token_headers
                               )
        t_id = res_task.json().get("id") or res_task.json().get("_id")
        client.put(f"/tasks/{t_id}", json={"completed": True}, headers=normal_user_token_headers)

    # 2. Ahora que tiene los 100 puntos exactos, compra el color
    response = client.post(
        "/store/buy-color",
        json={"hex_color": "#00FF00"},
        headers=normal_user_token_headers
    )

    # 3. VERIFICACIÓN: El servidor debe responder 200 OK
    assert response.status_code == 200
    assert "desbloqueado con éxito" in response.json()["message"]

    # 4. INVENTARIO: Verificamos que el color aparece en su lista
    res_inv = client.get("/store/my-inventory", headers=normal_user_token_headers)
    assert "#00FF00" in res_inv.json()["colors"]