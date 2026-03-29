from beanie import Document, Indexed, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id_fast

class SettingBase(BaseModel):
    # Define la personalización básica/general de la app para un usuario.
    # Foreign Key a Users: Relación 1 a 1 (un usuario = una configuración)
    user_id: Indexed(int, unique=True)

    # Foreign Key a Themes: Identificador del tema general de la app
    theme_id: int

    # Color de acento (opcional). Usamos Optional[str]
    # para que no sea un campo obligatorio. Ejemplo: "#FF5733"
    accent_color: Optional[str] = None

    # Idioma de la aplicación. Le ponemos "es" por defecto para que
    # si el usuario no envía nada, asuma español.
    lenguaje: str = "es"

class Setting(Document, SettingBase):
    # Modelo exacto que se guarda en la colección "settings" de MongoDB.
    # Primary Key: Reemplaza el ObjectId por nuestro int autoincremental
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        name = "settings"

    # Hook para asignar el ID autoincremental antes de guardar
    @before_event(Insert)
    def assign_id(self):
        if self.id is None:
            self.id = get_next_id_fast()


class SettingCreate(SettingBase):
    # Esquema para crear la configuración (POST).
    # Por ahora es idéntico a EventBase, pero tenerlo separado permite
    # añadir campos en el futuro que solo sean necesarios al crear.
    pass

class SettingUpdate(BaseModel):
    # Esquema para actualizar la configuración (PATCH).
    # Todos los campos son opcionales para permitir actualizaciones parciales.
    theme_id: Optional[int] = None
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None

class SettingOut(SettingBase):
    # Esquema que se devuelve al cliente con todos los datos.
    id: int # El ID generado es obligatorio en la respuesta

    model_config = ConfigDict(from_attributes=True)