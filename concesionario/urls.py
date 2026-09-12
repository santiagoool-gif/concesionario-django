

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("carros/", include("carros.urls")),
    path("clientes/", include("clientes.urls")),
    path("admin/", admin.site.urls),
]