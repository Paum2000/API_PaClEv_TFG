from beanie import Document
from pydantic import Field


class Counter(Document):
    id: str = Field(alias="_id")
    seq: int = 0

    class Settings:
        name = "counters"

async def get_next_id(sequence_name: str) -> int:
    counter = await Counter.get(sequence_name)
    if not counter:
        # Si no existe el contador para esta tabla, lo creamos
        counter = Counter(id=sequence_name, seq=0)
        await counter.insert()

    # Incrementamos y guardamos
    counter.seq += 1
    await counter.save()

    return counter.seq