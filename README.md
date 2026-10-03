# Concesionario Django + Microservicios Node.js

Proyecto final de Ingeniería de Software. La aplicación principal está construida con Django y contiene el CRUD de vehículos, características, clientes, un asistente con Gemini y el consumo de microservicios externos.

## Arquitectura final

```text
                         ┌── Node.js INSERTAR ───────┐
                         │                            │
Django + PostgreSQL ─────┼── Node.js ACTUALIZAR ─────┼── Operaciones CRUD
                         │                            │
                         └── Node.js ELIMINAR ───────┘

Django API de consulta
        │
        ├── microservicio Node.js primario
        │
        └── microservicio Node.js de respaldo
                 ↓
             resiliencia

Django API de inventario → Gemini → respuestas sobre datos actuales
```

## Rutas principales

- `/carros/` — inventario local
- `/carros/nuevo/` — crear carro
- `/carros/<id>/editar/` — actualizar carro
- `/carros/<id>/eliminar/` — eliminar carro
- `/carros/api/carros/` — JSON del inventario actual
- `/carros/api/carros/resiliente/` — consulta con respaldo
- `/carros/ia/` — asistente Gemini
- `/pokemon/` — consumo del microservicio Pokémon
- `/admin/` — administración Django

## Microservicios Node.js

### Insertar
- POST `/carros`
- GET `/health`
- Swagger: `/docs`

### Actualizar
- PUT `/carros/:id`
- GET `/carros` — consulta para resiliencia
- GET `/health`
- Swagger: `/docs`

### Eliminar
- DELETE `/carros/:id`
- GET `/carros` — consulta de respaldo
- GET `/health`
- Swagger: `/docs`

Cada microservicio tiene su propio `package.json`, `server.js` y documentación OpenAPI.

## Variables de entorno

Nunca subas `.env` al repositorio. Usa `.env.example` como plantilla.

Django necesita principalmente:

- `GEMINI_API_KEY`
- `GEMINI_MODEL`
- `SECRET_KEY`
- `INTERNAL_API_TOKEN`
- `DATABASE_URL` en producción
- `CARROS_API_URL`
- `NODE_INSERT_URL`
- `NODE_UPDATE_URL`
- `NODE_DELETE_URL`
- `READ_PRIMARY_URL`
- `READ_FALLBACK_URL`

Los microservicios Node.js necesitan:

- `PORT`
- `DJANGO_BASE_URL`
- `INTERNAL_API_TOKEN`

Los microservicios Flask de carros y Pokémon necesitan `MONGO_URI`.

## Ejecutar Django localmente

```cmd
venv\Scripts\activate
cd concesionario
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Para probar el CRUD a través de Node.js, inicia los tres microservicios en terminales separadas:

```cmd
cd microservicios_node\insertar
npm install
npm start
```

```cmd
cd microservicios_node\actualizar
npm install
npm start
```

```cmd
cd microservicios_node\eliminar
npm install
npm start
```

Luego copia cada `.env.example` como `.env` y verifica que `INTERNAL_API_TOKEN` sea igual al configurado en Django.

## Publicación en Render

El proyecto incluye `render.yaml` y `build.sh` para facilitar la publicación.

El Blueprint crea:

- 1 servicio web Django
- 1 PostgreSQL
- 3 servicios web Node.js

En Render: **New → Blueprint Instance → conectar el repositorio → Apply**.

Después agrega `GEMINI_API_KEY` como variable secreta del servicio Django. Cuando el servicio termine de desplegar, puedes cargar los datos de demostración desde Render Shell con:

```bash
python manage.py loaddata carros/fixtures/initial_data.json
``` Render también puede generar `SECRET_KEY` e `INTERNAL_API_TOKEN` automáticamente mediante el Blueprint.

> El PostgreSQL gratuito de Render está pensado para pruebas y actualmente expira después de 30 días. Para una entrega académica de corto plazo funciona, pero si el proyecto debe permanecer disponible durante más tiempo conviene usar una base de datos externa con un plan gratuito que no tenga ese vencimiento.

## Importante

El proyecto que se entrega al repositorio no contiene las credenciales reales de Gemini ni MongoDB. Antes de publicar, configura las variables de entorno en Render.
