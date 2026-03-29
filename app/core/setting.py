from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Define todas las variables de entorno y configuraciones de la app.
    # Al heredar de BaseSettings, Pydantic automáticamente buscará estas
    # variables en el entorno del sistema operativo o en un archivo .env.
    # Si estas variables NO están en tu archivo .env,
    # la aplicación usará estos valores de forma predeterminada.
    database_name: str = "agenda_db"
    app_name: str = "API (MongoDB)"

    # Pydantic es tan inteligente que si en tu .env pones DEBUG=True (texto),
    # él lo convertirá automáticamente a un booleano (bool) de Python.
    debug: bool = True

    # La URL de conexión por defecto apunta a tu base de datos local
    mongodb_url: str = "mongodb://localhost:27017"

    # SettingsConfigDict le dice a Pydantic como y de donde leer los datos:
    # 1. env_file=".env": Busca un archivo llamado ".env" en la raíz del proyecto.
    # 2. env_file_encoding="utf-8": Asegura que lea bien caracteres especiales si los hay.
    # 3. extra="ignore": Si en .env hay otras variables, Pydantic las ignorará
    # en lugar de lanzar un error y colgar la app.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Al crear la instancia aquí, Pydantic lee el .env una sola vez al arrancar.
# Luego, en cualquier otro archivo del proyecto solo tienes que importar 'settings'
# y tendremos acceso rápido y tipado settings.mongodb_url o settings.database_name.
settings = Settings()