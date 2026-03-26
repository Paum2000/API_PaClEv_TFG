from pydantic import BaseModel
from typing import Optional

# --- 1. THEME BASE (El ADN del tema) ---
# Define que lo único que necesitamos para identificar un tema visualmente
# su nombre.
class ThemeBase(BaseModel):
    name: str

# --- 2. THEME CREATE (Creación de nuevos temas) ---
# Se usa cuando un administrador quiere dar de alta un nuevo estilo.
# Hereda 'name' de ThemeBase. No necesita más campos por ahora.
class ThemeCreate(ThemeBase):
    pass

# --- 3. THEME OUT (Respuesta al Frontend) ---
# Es el objeto que el frontend recibe para llenar, por ejemplo,
# un menú desplegable de "Selecciona tu tema".
class ThemeOut(ThemeBase):
    id: int # El ID es fundamental para que el frontend sepa cuál elegir.

    # Permite que Pydantic lea los datos desde un objeto de la base de datos.
    class Config:
        from_attributes = True

# --- 4. THEME UPDATE (Modificación) ---
# Se usa para cambiar el nombre de un tema existente.
# Al ser 'Optional', permite enviar el cambio de forma segura.
class ThemeUpdate(BaseModel):
    name: Optional[str] = None