from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_name: str
    app_name: str
    debug: bool = False

    class Settings:
        env_file = ".env"
        extra = "ignore"

settings = Settings()