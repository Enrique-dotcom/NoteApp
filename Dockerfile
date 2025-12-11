# 1. Usa una imagen base oficial de Python
FROM python:3.11-slim

# 2. Establece el directorio de trabajo
WORKDIR /usr/src/app

# 3. Instalar dependencias del sistema necesarias
# Esto es crucial para que psycopg2-binary se compile e instale correctamente.
# Incluye el cliente de postgresql para la conexión (libpq-dev) y herramientas de compilación.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        musl-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia el archivo de dependencias
COPY requirements.txt .

# 5. Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia el resto del código de la aplicación (app.py, config.py, templates, static)
COPY . .

# 6a. Convierte los finales de línea de CRLF a LF (importante en Windows)
RUN apt-get update && apt-get install -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN dos2unix wait-for-it.sh
RUN chmod +x wait-for-it.sh

# 7. Define el puerto que la aplicación Gunicorn usará
EXPOSE 8000

# 8. Comando para correr la aplicación con Gunicorn (servidor WSGI de producción)
# Es importante usar 0.0.0.0 para que el contenedor escuche peticiones externas.
CMD python init_db.py && gunicorn --bind 0.0.0.0:8000 app:app