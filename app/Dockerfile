# Imagen base ligera de Python
FROM python:3.11-slim

# Variables de entorno para mejor experiencia en contenedor
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Dependencias del sistema para psycopg2 y compilacion
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Puerto expuesto por gunicorn
EXPOSE 5500

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias Python primero (mejor cache de Docker)
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la app
COPY static /app/static
COPY templates /app/templates
COPY wsgi.py /app/

# Healthcheck simple
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -fsS http://localhost:5500/ || exit 1

# Comando por defecto: gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5500", "--workers", "2", "--timeout", "120", "wsgi:app"]
