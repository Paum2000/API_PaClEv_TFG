from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id

# --- 1. CLASE BASE (Atributos comunes) ---
# Extraemos los colores, idiomas y las referencias a otras colecciones.
class SettingBase(BaseModel):
    accent_color: str = "#000000"
    lenguaje: str = "es"
    user_id: int
    theme_id: int

# --- 2. MODELO DE COLECCIÓN (La Base de Datos en Mongo) ---
# Hereda de Document y de SettingBase. Añade el ID y el hook.
class Setting(Document, SettingBase):
    id: Optional[int] = Field(default=None)

    class Settings:
        name = "settings"

    # Generador automático del ID numérico al insertar
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            self.id = await get_next_id("settings_id")

# --- 3. MODELO DE CREACIÓN (POST) ---
# Hereda todos los campos tal cual.
class SettingCreate(SettingBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (PUT) ---
# Va por libre para que todos los campos sean opcionales.
# Nota: No incluimos 'user_id' porque un usuario no debería
# poder transferir su configuración a otro usuario distinto.
class SettingUpdate(BaseModel):
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None
    theme_id: Optional[int] = None

# --- 5. MODELO DE SALIDA (Respuesta GET de la API) ---
# Hereda de SettingBase y le añade el ID para el frontend.
class SettingOut(SettingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)