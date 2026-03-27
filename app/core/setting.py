from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ya no es un archivo .db, es solo el nombre lógico que tendrá en MongoDB
    database_name: str = "agenda_db"
    app_name: str = "Mi Agenda API (MongoDB)"
    debug: bool = True

    # ¡NUEVO! La dirección donde escucha tu servidor MongoDB local
    mongodb_url: str = "mongodb://localhost:27017"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()