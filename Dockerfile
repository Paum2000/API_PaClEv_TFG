# 1. Imagen base de Python ligera
FROM python:3.11-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalamos dependencias del sistema para psycopg2 (Postgres)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 4. Copiamos los requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código de tu carpeta actual a /app
COPY . .

# 6. Comando para arrancar la API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]