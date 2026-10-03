# Microservicios Node.js - Concesionario

Tres microservicios Express, uno por operación:

- `insertar`: POST `/carros`
- `actualizar`: PUT `/carros/:id`
- `eliminar`: DELETE `/carros/:id`

Los tres exponen documentación Swagger en `/docs`.

El microservicio de actualización expone además `GET /carros` y el de eliminación expone `GET /carros` para permitir la estrategia de resiliencia del proyecto: Django consulta el primero y, si falla, consulta el segundo.

Los microservicios delegan la persistencia al API interno de Django. Así el proyecto conserva una sola fuente de verdad para los datos y los microservicios encapsulan las operaciones solicitadas por el profesor.
