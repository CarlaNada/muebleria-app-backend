# Imagen base con Python 3.12 y uv
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Configuración de Python y uv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_NO_DEV=1

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen --no-dev --no-install-project

# Copiar el código del proyecto
COPY . .

# Sincronizar el proyecto
RUN uv sync --frozen --no-dev

# Puerto del backend
EXPOSE 8000

# Iniciar Django
CMD ["sh", "-c", "uv run --no-sync python manage.py migrate && uv run --no-sync python manage.py collectstatic --noinput && uv run --no-sync gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
