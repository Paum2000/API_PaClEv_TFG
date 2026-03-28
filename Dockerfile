FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fíjate que el comando ahora es uvicorn (el servidor real), no pytest
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]