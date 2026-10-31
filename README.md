# Mueblería Arboleda — Backend

Backend desarrollado para la Evaluación Final Integradora 2026 de Ingeniería de Software. Consiste en una API REST construida con Django y Django REST Framework para gestionar el catálogo, los clientes y las ventas de una mueblería, preparada para integrarse con un frontend en Next.js.

## Integrantes

- Carla Nadalig
- Mateo Urquiza
- Sebastián Maldonado

## Objetivo

Desarrollar un sistema que permita administrar productos, categorías, materiales, clientes, direcciones, pedidos, pagos y envíos mediante una API REST.

## Tecnologías utilizadas

- **Python 3.12 y Django 5.2:** desarrollo del backend.
- **Django REST Framework:** API REST y ViewSets.
- **SQLite:** base de datos relacional.
- **SimpleJWT y SessionAuthentication:** autenticación.
- **django-filter:** filtros, búsqueda y ordenamiento.
- **drf-spectacular:** documentación Swagger/OpenAPI.
- **django-cors-headers:** integración con el frontend.
- **django-environ:** variables de entorno.
- **uv:** gestión de dependencias.
- **Docker y Docker Compose:** ejecución en contenedores.
- **Git y GitHub:** control de versiones y trabajo colaborativo.

Las dependencias se encuentran definidas en `pyproject.toml` y `uv.lock`.

## Funcionalidades principales

- CRUD de categorías, materiales, productos, clientes y ventas.
- Autenticación JWT y por sesiones, con permisos de acceso.
- Filtros, búsqueda, ordenamiento y paginación.
- Serializadores anidados y acciones personalizadas (`@action`).
- Administración mediante Django Admin.
- Documentación interactiva con Swagger.
- Página HTML de bienvenida.
- Pruebas automatizadas de la API.

## Modelado de la base de datos

El sistema cuenta con **10 modelos propios**, distribuidos en tres aplicaciones:

- **Catálogo:** Categoria, Material, Producto y ProductoMaterial.
- **Clientes:** Cliente y Direccion.
- **Ventas:** Pedido, ItemPedido, Pago y Envio.

Los modelos utilizan relaciones `ForeignKey`, `OneToOneField` y `ManyToManyField`, mediante el ORM de Django.

**[Ver diagrama y documentación del modelado](docs/modelado.md)**

## Organización del trabajo

Se utiliza un flujo de ramas con `main`, `develop` y ramas `feature/`, integradas mediante Pull Requests y revisión de código.

Las convenciones de trabajo están documentadas en [CONTRIBUTING.md](CONTRIBUTING.md).

## Puesta en marcha local

### Requisitos

- Python 3.12
- uv
- Git

### Instalación

Clonar el repositorio e instalar las dependencias:

```bash
git clone https://github.com/CarlaNada/muebleria-app-backend.git
cd muebleria-app-backend
uv sync
```

Crear el archivo de variables de entorno:

```bash
cp .env.example .env
```

Configurar `SECRET_KEY`, `DEBUG` y `ALLOWED_HOSTS` en `.env`. Este archivo no debe subirse al repositorio.

Aplicar migraciones e iniciar el servidor:

```bash
uv run python manage.py migrate
uv run python manage.py runserver
```

La aplicación estará disponible en http://127.0.0.1:8000/.

Para acceder al panel administrativo, crear un superusuario:

```bash
uv run python manage.py createsuperuser
```

## Ejecución con Docker

Se requiere tener Docker y Docker Compose instalados, además del archivo `.env` configurado.

```bash
# Construir la imagen
docker compose build

# Aplicar las migraciones
docker compose run --rm backend uv run --no-sync python manage.py migrate

# Iniciar el backend
docker compose up -d

# Detener los contenedores
docker compose down
```

El backend estará disponible en http://127.0.0.1:8000/.

SQLite utiliza un volumen Docker para conservar los datos entre reinicios. Esta configuración está destinada al desarrollo y pruebas locales.

## Endpoints principales

| Recurso | Endpoint |
|---|---|
| Obtener JWT | `POST /api/token/` |
| Renovar JWT | `POST /api/token/refresh/` |
| Usuario actual | `GET /api/usuario-actual/` |
| Categorías | `/api/catalogo/categorias/` |
| Materiales | `/api/catalogo/materiales/` |
| Productos | `/api/catalogo/productos/` |
| Productos destacados | `/api/catalogo/productos/destacados/` |
| Productos disponibles | `/api/catalogo/productos/disponibles/` |
| Clientes | `/api/clientes/` |
| Direcciones | `/api/direcciones/` |
| Pedidos | `/api/ventas/pedidos/` |
| Ítems, pagos y envíos | `/api/ventas/items/`, `/pagos/`, `/envios/` |
| Cancelar pedido | `POST /api/ventas/pedidos/{id}/cancelar/` |

El catálogo permite consultas públicas y restringe las modificaciones a administradores. Los recursos de clientes y ventas aplican autenticación y permisos según el usuario.

Los productos admiten filtros por `categoria`, `activo` y `destacado`, además de parámetros de búsqueda y ordenamiento.

## Documentación de la API

- **Swagger:** http://127.0.0.1:8000/api/docs/
- **OpenAPI:** http://127.0.0.1:8000/api/schema/
- **Django Admin:** http://127.0.0.1:8000/admin/

## Pruebas

Ejecutar todas las pruebas automatizadas:

```bash
uv run python manage.py test
```

Verificar la configuración y las migraciones:

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
```

**Último resultado de integración:** 12 pruebas automatizadas aprobadas, incluyendo permisos del catálogo, acceso a clientes y validaciones de ventas.

También se realizaron pruebas manuales de endpoints, filtros y autenticación utilizando Thunder Client.
