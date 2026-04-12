import time
import random

# 1735689600 es el timestamp de 01-01-2025 00:00:00
CUSTOM_EPOCH = 1735689600

def get_next_id_fast() -> int:
    # 1. Obtenemos segundos actuales y restamos nuestro inicio
    seconds_since_epoch = int(time.time() - CUSTOM_EPOCH)

    # 2. Multiplicamos por 100 para dejar espacio a dos dígitos aleatorio
    unique_id = (seconds_since_epoch * 100) + random.randint(0, 99)

    return unique_id