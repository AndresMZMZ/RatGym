FROM python:3.11-slim

WORKDIR /app

# Instalamos dependencias primero para aprovechar el cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto
COPY . .

# Exponemos el puerto del servicio
EXPOSE 3006

# Variables de entorno importantes
ENV PYTHONPATH=/app

# Comando corregido para arrancar desde src.main
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3006"]