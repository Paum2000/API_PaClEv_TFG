from beanie import Document
from pydantic import Field

# --- MODELO DE CONTADOR (Patrón Auto-incremental en NoSQL) ---
# En MongoDB, los IDs por defecto son ObjectIds (cadenas alfanuméricas complejas).
# Como nuestra API y el Frontend esperan IDs numéricos enteros (1, 2, 3...),
# usamos esta colección especial para llevar la cuenta de por qué número va cada entidad.
class Counter(Document):
    # El ID de este documento será el nombre de la secuencia (ej: "users_id", "tasks_id").
    # Usamos Field(alias="_id") para decirle a Mongo que use este string como su clave principal real.
    id: str = Field(alias="_id")

    # El valor actual del contador.
    seq: int = 0

    class Settings:
        # Todos los contadores (de usuarios, tareas, eventos...) estaran juntos en esta colección.
        name = "counters"


# --- FUNCIÓN GENERADORA DE IDs ---
# Esta función asíncrona es llamada automáticamente por los "Hooks" (@before_event)
# de nuestros modelos justo antes de ser insertados en la base de datos.
async def get_next_id(sequence_name: str) -> int:
    # 1. Buscamos en la base de datos si ya existe un contador para esta tabla en concreto.
    counter = await Counter.get(sequence_name)

    # 2. Si es la primera vez que insertamos un documento de este tipo, el contador no existirá.
    if not counter:
        # Lo creamos desde cero.
        counter = Counter(id=sequence_name, seq=0)
        await counter.insert()

    # 3. Sumamos 1 a la secuencia actual.
    counter.seq += 1

    # 4. Guardamos el nuevo valor en la base de datos para que el siguiente ID no se repita.
    await counter.save()

    # 5. Devolvemos el número entero, listo para ser asignado al nuevo documento.
    return counter.seq