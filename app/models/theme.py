from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

# --- 1. CLASE BASE (El nombre del tema) ---
# Define la estructura mínima de un tema.
class ThemeBase(SQLModel):
    name: str

# --- 2. MODELO DE TABLA (La base de datos) ---
# Esta clase crea la tabla "themes" en la base de datos.
class Theme(ThemeBase, table=True):
    __tablename__ = "themes"
    # ID autoincremental para identificar cada tema.
    id: Optional[int] = Field(default=None, primary_key=True)

    # RELACIÓN: Un tema puede estar aplicado en muchas configuraciones de usuarios.
    # Es una relación de "uno a muchos": Un Tema -> Muchas Settings.
    settings: List["Setting"] = Relationship(back_populates="theme")

# --- 3. MODELO DE CREACIÓN (Input) ---
# Se usa para añadir nuevos temas al sistema.
class ThemeCreate(ThemeBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (PATCH) ---
# Permite cambiar el nombre de un tema existente sin afectar su ID.
class ThemeUpdate(SQLModel):
    name: Optional[str] = None

# --- 5. MODELO DE SALIDA (Output) ---
# Lo que el frontend recibe.
# Es útil para llenar selectores (dropdowns) en la interfaz de usuario.
class ThemeOut(ThemeBase):
    id: int