from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ThemeBase(BaseModel):
    # Define la estructura básica de un tema visual.
    name: str

class ThemeCreate(ThemeBase):
    # Esquema para cuando el administrador crea un tema nuevo.
    pass

class ThemeOut(ThemeBase):
    # Lo que FastAPI devuelve al cliente cuando pide la lista de temas.
    # Hereda el 'name' y le añade el 'id' generado por la base de datos.
    id: int= Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class ThemeUpdate(BaseModel):
    # Esquema para modificar un tema que ya existe.
    # Como siempre en los Update, los campos se vuelven opcionales (Optional).
    name: Optional[str] = None