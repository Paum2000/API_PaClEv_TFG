from fastapi import FastAPI
from app.routers import users, tasks, events, settings, themes

app = FastAPI(title="PaClEv API")

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(events.router)
app.include_router(settings.router)
app.include_router(themes.router)

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de tu Agenda!"}