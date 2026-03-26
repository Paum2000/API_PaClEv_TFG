from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 1. Le damos valores por defecto por si no encuentra el .env
    database_name: str = "agenda.db"
    app_name: str = "PaClEv API"
    debug: bool = True

    # 2. Le decimos a Pydantic que lea automáticamente el archivo .env (sintaxis de Pydantic v2)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()