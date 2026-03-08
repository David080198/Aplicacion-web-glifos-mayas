# Imagen base con Python 3.11 slim para menor tamaño
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Puerto de la aplicación
EXPOSE 5500

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias primero (para cache de Docker)
COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY static /app/static
COPY templates /app/templates
COPY wsgi.py /app

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5500", "--workers", "2", "--timeout", "120", "wsgi:app"]
