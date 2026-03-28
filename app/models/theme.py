from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id

# --- 1. CLASE BASE (Atributos comunes) ---
# Contiene los datos que comparten la base de datos y la API.
class ThemeBase(BaseModel):
    name: str

# --- 2. MODELO DE COLECCIÓN (La Base de Datos en Mongo) ---
# Hereda de Document (Beanie) y ThemeBase (para tener el 'name').
class Theme(Document, ThemeBase):
    id: Optional[int] = Field(default=None)

    class Settings:
        name = "themes"

    # Generador automático del ID numérico al insertar
    @before_event(Insert)
    async def assign_id(self):
        if not self.id:
            self.id = await get_next_id("themes_id")

# --- 3. MODELO DE CREACIÓN (POST) ---
# Como al crear un tema solo necesitamos el nombre, hereda directamente
# de ThemeBase y no hace falta añadirle nada más.
class ThemeCreate(ThemeBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (PUT) ---
# Este va por libre (hereda de BaseModel) porque para actualizar
# necesitamos que el nombre sea opcional (por si en el futuro añades más campos y solo quieres actualizar uno).
class ThemeUpdate(BaseModel):
    name: Optional[str] = None

# --- 5. MODELO DE SALIDA (Respuesta GET de la API) ---
# Hereda el 'name' de ThemeBase y le añade el ID para devolverlo al Frontend.
class ThemeOut(ThemeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)