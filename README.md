# Mueblería — Backend
Repositorio del backend para la Evaluación Final Integradora 2026 de Ingeniería de Software. Se desarrollará con Django y expondrá una API REST para que la consuma el frontend de Programación III.

# Integrantes

- Carla Nadalig
- Mateo Urquiza
- Sebastián Maldonado

# Objetivo

- Planificar y construir un sistema para gestionar el catálogo y las ventas de una mueblería.

# Tecnologías previstas
- Python y Django.
- Django REST Framework para la API REST.
- uv para gestionar dependencias y el entorno.
- Docker para ejecutar el backend.
- CORS y autenticación para permitir la futura integración con Next.js.

Para el desarrollo inicial se usa SQLite. Las dependencias están declaradas en pyproject.toml y uv.lock.

# Alcance previsto

- Gestión de categorías, materiales y productos.
- Gestión de clientes, direcciones, pedidos, pagos y envíos.
- Autenticación, permisos, paginación, filtros y documentación de API.
- Panel de administración de Django.
- Vista principal de bienvenida.

# Diseño inicial

La propuesta de modelos y relaciones está en docs/modelado.md. Es un diseño preliminar que el equipo debe revisar antes de implementar las migraciones.

# Organización del trabajo

El flujo de ramas, la convención de commits y las reglas para Pull Requests están en CONTRIBUTING.md.

# Puesta en marcha

### Requisitos

- Python 3.12
- `uv`
- Git

### Clonar el repositorio

```bash
git clone https://github.com/CarlaNada/muebleria-app-backend.git
cd muebleria-app-backend
```

### Instalar las dependencias

```bash
uv sync
```

### Preparar la base de datos

```bash
uv run python manage.py migrate
```

### Iniciar el servidor

```bash
uv run python manage.py runserver
```

Abrí `http://127.0.0.1:8000/` en el navegador. Para detener el servidor, presioná `Ctrl+C`.
```

`uv sync` instala las dependencias declaradas en el proyecto; `migrate` prepara la base de datos y `runserver` inicia el servidor de desarrollo.