from locust import HttpUser, task, between
import random
import time

class ComportamientoUsuarioAPI(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1.0, 2.5)
    user_id_generado = None

    def on_start(self):
        """Se ejecuta una vez cuando el usuario virtual 'entra' a la app."""
        timestamp = time.time()
        email_unico = f"locust_{timestamp}_{random.randint(1, 99999)}@test.com"

        response = self.client.post("/users/", json={
            "user_name": "LocustUser",
            "email": email_unico,
            "password": "password_seguro"
        })

        # Minúsculo escudo protector: Solo guardamos el ID si todo salió bien (200 OK)
        # Si falla (ese 1%), este usuario simplemente no hará nada, pero no romperá el programa.
        if response.status_code == 200:
            self.user_id_generado = response.json().get("id") or response.json().get("_id")

    @task(3)
    def ver_mis_tareas(self):
        if self.user_id_generado:
            self.client.get(f"/tasks/user/{self.user_id_generado}", name="/tasks/user/[id]")

    @task(1)
    def crear_nueva_tarea(self):
        if self.user_id_generado:
            self.client.post("/tasks/", json={
                "title": f"Tarea Locust {random.randint(1, 100)}",
                "description": "Prueba de carga",
                "start_date": "2026-03-25T10:00:00",
                "priority": "Alta",
                "user_id": self.user_id_generado
            }, name="/tasks/ [POST]")