from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class SettingBase(BaseModel):
    # Define las propiedades estéticas y de localización básicas.
    # Son opcionales o tienen valores por defecto, por lo que el usuario
    # no está obligado a enviarlas al registrarse.
    user_id: Optional[int] = None
    theme_id: int
    # Color hexadecimal para detalles de la UI (ej: "#FF5733")
    accent_color: Optional[str] = None

    # Si el frontend no envía este dato, la base de datos asume español automáticamente.
    lenguaje: str = "es"

class SettingCreate(SettingBase):
    pass

class SettingOut(SettingBase):
    # Esto es exactamente lo que recibirá el frontend cuando pida la configuración.
    id: int = Field(alias="_id")        # El ID único de la configuración en Mongo

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class SettingUpdate(BaseModel):
    # Esquema exclusivo para modificar la configuración existente.
    # Todo es 'Optional' porque el usuario podría querer cambiar solo
    # el idioma sin tocar su color de acento o su tema.
    theme_id: Optional[int] = None
    accent_color: Optional[str] = None
    lenguaje: Optional[str] = None
