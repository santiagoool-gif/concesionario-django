from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:carro_id>/", views.detail, name="detail"),
    path("<int:carro_id>/results/", views.results, name="results"),
    path("<int:carro_id>/comprar/", views.comprar, name="comprar"),
    path("nube/", views.carros_nube, name="carros_nube"),
    path("anio/<int:anio>/", views.carros_por_anio, name="carros_por_anio"),
    path("ia/", views.ia_concesionario, name="ia_concesionario"),
]