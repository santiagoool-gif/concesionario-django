# Django - Carros (hasta Views)

Proyecto basado en la Parte 1 del tutorial oficial de Django 6.1:
https://docs.djangoproject.com/en/6.1/intro/tutorial01/

Se llegó hasta:
- Crear el proyecto.
- Crear la app `carros`.
- Crear la primera `view`.
- Crear `carros/urls.py`.
- Conectar `carros.urls` desde el URLconf principal.
- Ejecutar el servidor y comprobar `/carros/`.

## Requisito
Django 6.1 requiere Python 3.12 o posterior.

## Windows - instalación desde cero

Abre PowerShell o CMD y entra a la carpeta donde quieras guardar el proyecto.

```powershell
py --version
```

Crear entorno virtual:

```powershell
py -m venv venv
```

Activarlo en PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Si usas CMD:

```cmd
venv\Scripts\activate
```

Instalar Django:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Comprobar Django:

```powershell
python -m django --version
```

Debe mostrar:

```text
6.1
```

Entrar al proyecto:

```powershell
cd concesionario
```

Ejecutar migraciones iniciales:

```powershell
python manage.py migrate
```

Iniciar servidor:

```powershell
python manage.py runserver
```

Abrir:

http://127.0.0.1:8000/carros/

También puedes usar:

http://localhost:8000/carros/

## Detener servidor

En la terminal:

```text
CTRL + C
```

## Estructura

```text
concesionario/
├── manage.py
├── requirements.txt
├── README.md
├── concesionario/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── carros/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── migrations/
        └── __init__.py
```
