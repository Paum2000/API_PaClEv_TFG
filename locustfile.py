from locust import HttpUser, task, between
import random

class ComportamientoUsuarioAPI(HttpUser):
    host = "http://localhost:8000"
    # Pausa entre 1 y 2.5 segundos entre cada petición (simula lectura humana)
    wait_time = between(1.0, 2.5)
    user_id_generado = None

    def on_start(self):
        """Se ejecuta una vez cuando el usuario virtual 'entra' a la app."""
        # Creamos un usuario de prueba en la BD para que este usuario virtual juegue
        num_random = random.randint(1, 100000)
        response = self.client.post("/users/", json={
            "user_name": f"LocustUser_{num_random}",
            "email": f"locust_{num_random}@test.com",
            "password": "password_seguro"
        })
        if response.status_code == 200:
            self.user_id_generado = response.json()["id"]

    @task(3) # Mayor probabilidad: El usuario consulta sus tareas
    def ver_mis_tareas(self):
        if self.user_id_generado:
            self.client.get(f"/tasks/user/{self.user_id_generado}", name="/tasks/user/[id]")

    @task(1) # Menor probabilidad: El usuario crea una tarea nueva
    def crear_nueva_tarea(self):
        if self.user_id_generado:
            self.client.post("/tasks/", json={
                "title": f"Tarea generada por Locust {random.randint(1, 100)}",
                "description": "Prueba de carga",
                "start_date": "2026-03-25T10:00:00",
                "done_date": "2026-03-26T10:00:00",
                "priority": "Alta",
                "user_id": self.user_id_generado
            }, name="/tasks/ [POST]")