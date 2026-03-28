from locust import HttpUser, task, between
import uuid

class ComportamientoUsuarioAPI(HttpUser):
    host = "http://localhost:8000"
    # Pausa simulando la lectura humana
    wait_time = between(1.0, 2.5)
    user_id_generado = None

    def on_start(self):
        """Se ejecuta una vez cuando el usuario virtual 'entra' a la app."""
        # Usamos UUID para garantizar 100% un email y nombre únicos
        id_unico = uuid.uuid4().hex[:8]

        response = self.client.post("/users/", json={
            "user_name": f"LocustUser_{id_unico}",
            "email": f"locust_{id_unico}@test.com",
            "password": "password_seguro"
        })

        # Solo si se crea correctamente, guardamos su ID para las tareas
        if response.status_code == 200:
            # Dependiendo de tu BD (SQL/Mongo), el ID puede venir en distinto formato
            # Lo extraemos de forma segura
            self.user_id_generado = response.json().get("id")

    @task(3)
    def ver_mis_tareas(self):
        if self.user_id_generado:
            self.client.get(f"/tasks/user/{self.user_id_generado}", name="/tasks/user/[id]")

    @task(1)
    def crear_nueva_tarea(self):
        if self.user_id_generado:
            # Generamos un identificador único también para el título de la tarea
            id_tarea = uuid.uuid4().hex[:4]
            self.client.post("/tasks/", json={
                "title": f"Tarea generada {id_tarea}",
                "description": "Prueba de carga",
                "start_date": "2026-03-25T10:00:00",
                "done_date": "2026-03-26T10:00:00",
                "priority": "Alta",
                "user_id": self.user_id_generado
            }, name="/tasks/ [POST]")