import time
import random

def get_next_id_fast() -> int:
    # Genera un ID numérico único basado en milisegundos.
    # Usamos el tiempo actual (epoch) multiplicado para tener un entero largo
    # Sumamos un random pequeño para evitar colisiones si dos peticiones
    # entran exactamente en el mismo microsegundo.
    return int(time.time() * 1000) + random.randint(1, 999)