from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "agenda_db"
    db_type: str = "postgresql+psycopg2"
    api_host: str = "0.0.0.0"
    debug: bool = False

    # Configuración para Pydantic v2
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

config = Config()