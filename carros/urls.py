from django.urls import path
from . import views

app_name = "carros"

urlpatterns = [
    path("", views.index, name="index"),
    path("nuevo/", views.crear_carro, name="crear"),
    path("nube/", views.carros_nube, name="carros_nube"),
    path("anio/<int:anio>/", views.carros_por_anio, name="carros_por_anio"),
    path("ia/", views.ia_concesionario, name="ia_concesionario"),

    # APIs publicas
    path("api/carros/", views.api_carros, name="api_carros"),
    path("api/carros/resiliente/", views.api_carros_resiliente, name="api_carros_resiliente"),

    # APIs internas consumidas por los microservicios Node.js
    path("api/interno/carros/crear/", views.api_interno_crear, name="api_interno_crear"),
    path("api/interno/carros/<int:carro_id>/actualizar/", views.api_interno_actualizar, name="api_interno_actualizar"),
    path("api/interno/carros/<int:carro_id>/eliminar/", views.api_interno_eliminar, name="api_interno_eliminar"),

    # Caracteristicas
    path("<int:carro_id>/caracteristica/nueva/", views.agregar_caracteristica, name="agregar_caracteristica"),
    path("caracteristica/<int:caracteristica_id>/editar/", views.editar_caracteristica, name="editar_caracteristica"),
    path("caracteristica/<int:caracteristica_id>/eliminar/", views.eliminar_caracteristica, name="eliminar_caracteristica"),

    # Carros
    path("<int:carro_id>/results/", views.results, name="results"),
    path("<int:carro_id>/comprar/", views.comprar, name="comprar"),
    path("<int:carro_id>/editar/", views.editar_carro, name="editar"),
    path("<int:carro_id>/eliminar/", views.eliminar_carro, name="eliminar"),
    path("<int:carro_id>/", views.detail, name="detail"),
]
