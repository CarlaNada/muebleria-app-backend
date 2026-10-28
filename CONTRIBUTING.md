Este repositorio contiene el backend de la EFI 2026 de Ingeniería de Software. Se desarrollará con Django y Django REST Framework y expondrá una API REST para el frontend independiente del proyecto.

# Flujo de ramas

Usamos un GitFlow simplificado:

- main: versión estable para la entrega.
- develop: rama de integración.
- feature/back-<tarea>: nuevas funcionalidades.
- fix/back-<bug>: correcciones.

Ejemplos: feature/back-productos-viewset, feature/back-autenticacion-jwt y fix/back-filtro-pedidos.

Las ramas de trabajo se crean desde develop y se integran mediante Pull Request hacia develop. La versión de entrega llega a main mediante un Pull Request desde develop.

Antes de empezar una tarea:
```bash
git switch develop
git pull origin develop
git switch -c feature/back-productos-viewset
```
Cada rama debe enfocarse en una tarea. No se trabaja directamente sobre main ni develop.

# Convención de commits

Todos los commits deben respetar Conventional Commits:

<tipo>(<área>): <descripción breve>

Tipos habituales:

- feat: funcionalidad nueva.
- fix: corrección de un error.
- docs: documentación.
- test: pruebas.
- refactor: reorganización sin cambiar el comportamiento.
- chore: configuración o mantenimiento.

Ejemplos:
```bash
feat(api): agregar viewset de pedidos
fix(auth): corregir duración del token JWT
docs(readme): documentar el modelado de datos
test(productos): agregar pruebas de filtros
```
Usar descripciones claras y breves. No incluir claves, tokens, contraseñas ni datos personales en los commits.

#Pull Requests

- Todo cambio que llegue a develop o main debe integrarse mediante Pull Request.
- Está prohibido hacer push directo a main o develop.
- Cada Pull Request hacia develop requiere la aprobación de al menos un integrante distinto del autor antes del merge.
- Los Pull Requests hacia main también deben revisarse y aprobarse.
- El PR debe explicar qué cambia, cómo se verificó y qué tarea del equipo resuelve.
- Antes de solicitar revisión, actualizar la rama con develop, resolver conflictos y ejecutar las verificaciones disponibles.
- Mantener los PR pequeños y enfocados. Si el cambio afecta la API, describir los endpoints o contratos que modifica.

# Revisión de código

- Antes de aprobar un PR, comprobar que:
- Cumple la tarea acordada y respeta el diseño de docs/modelado.md.
- Los endpoints tienen autenticación y permisos adecuados.
- Los cambios de modelos incluyen las migraciones necesarias y fueron coordinados con el equipo.
- No incorpora secretos, archivos locales ni configuraciones personales.
- Se actualizaron la documentación y las pruebas afectadas, cuando corresponda.

# Coordinación

Coordinar los cambios que puedan afectar archivos compartidos, como settings.py, urls.py, la configuración de Docker y las migraciones. Definir entre los tres integrantes quién integra esos cambios. Antes de cerrar una tarea que afecte la API, confirmar con el equipo de frontend las rutas, los formatos de respuesta y la autenticación.