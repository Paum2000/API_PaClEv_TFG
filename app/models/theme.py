from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.models.counter import get_next_id_fast

class ThemeBase(BaseModel):
    # Define la estructura básica de un tema visual para la app.
    # Contiene la información mínima que comparten la BD y la API.
    # Ejemplo: name = "Dark Mode", "Ocean", "Cyberpunk", etc.
    name: str

class Theme(Document, ThemeBase):
    # Este es el modelo real que interactúa con la base de datos.
    # Hereda el 'name' de ThemeBase y añade configuraciones de Mongo.
    # Usamos el alias="_id" para que reemplace la clave primaria de MongoDB por defecto.
    id: Optional[int] = Field(default=None, alias="_id")

    class Settings:
        # Los documentos se guardarán en la colección "themes"
        name = "themes"

    # Este gancho se dispara justo antes de insertar el documento en Mongo
    @before_event(Insert)
    def assign_id(self):
        # Genera y asigna el identificador numérico único antes de guardarlo por primera vez.
        if self.id is None:
            self.id = get_next_id_fast()

class ThemeCreate(ThemeBase):
    # Esquema que recibe FastAPI cuando haces un POST.
    # Hereda de ThemeBase, así que solo exige el 'name'.
    pass

class ThemeUpdate(BaseModel):
    # Esquema para actualizar el tema (PATCH/PUT).
    # Va por libre (hereda de BaseModel) para que 'name' sea opcional.
    # Esto es útil por si en el futuro añades cosas como "font_family"
    # y quieres poder actualizar solo una cosa a la vez.
    name: Optional[str] = None

class ThemeOut(ThemeBase):
    # Esquema de respuesta de la API hacia el frontend/cliente.
    # Hereda el 'name' de la base y le incrusta el ID generado.
    id: int # El frontend necesita este ID para saber qué tema aplicar

    # Le dice a Pydantic cómo transformar el objeto de Beanie a un JSON limpio
    model_config = ConfigDict(from_attributes=True)