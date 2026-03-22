from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

# --- 1. CLASE BASE (Los cimientos) ---
# Define qué "ajustes" existen en tu app.
# Se usa para heredar estos campos a las demás clases y no repetir 'accent_color', etc.
class SettingBase(SQLModel):
    accent_color: Optional[str] = None  # Color de énfasis de la interfaz (ej. "#FF5733")
    lenguaje: str = "es"               # Idioma por defecto (Español)
    user_id: int = Field(foreign_key="users.id")   # Relación obligatoria: ¿A qué usuario pertenecen?
    theme_id: int = Field(foreign_key="themes.id") # Relación obligatoria: ¿Qué tema visual usa?

# --- 2. MODELO DE TABLA (La realidad en el disco duro) ---
# Esta es la clase que SQLModel usa para crear la tabla "settings" en la base de datos.
class Setting(SettingBase, table=True):
    __tablename__ = "settings"
    # El ID es opcional aquí porque al crear el objeto aún no existe en la DB (se genera solo)
    id: Optional[int] = Field(default=None, primary_key=True)

    # RELACIONES: Permiten acceder a los datos del Usuario y del Tema
    # directamente (ej. setting.user.name) sin hacer otra consulta manual.
    user: Optional["User"] = Relationship(back_populates="settings")
    theme: Optional["Theme"] = Relationship(back_populates="settings")

# --- 3. MODELO DE CREACIÓN (Registro inicial) ---
# Se usa cuando un usuario nuevo se registra y le asignas sus ajustes iniciales.
class SettingCreate(SettingBase):
    pass

# --- 4. MODELO DE ACTUALIZACIÓN (El panel de "Ajustes") ---
# Al ser todos 'Optional', el usuario no tiene que enviar toda su configuración de nuevo.
class SettingUpdate(SQLModel):
    theme_id: Optional[int] = None
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None

# --- 5. MODELO DE SALIDA (Lo que ve el Frontend) ---
# Cuando el frontend pide "dame los ajustes del usuario 5", tú devuelves esto.
# Aquí el ID es obligatorio (int) porque si sale de la DB, el ID ya existe sí o sí.
class SettingOut(SettingBase):
    id: int