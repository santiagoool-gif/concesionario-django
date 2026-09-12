from django.http import HttpResponse
from .models import Cliente


def index(request):
    clientes = Cliente.objects.all()

    texto = "<h1>Concesionario</h1>"
    texto += "<h2>Clientes registrados</h2>"

    for cliente in clientes:
        texto += f"<p>👤 {cliente.nombre} - {cliente.edad} años</p>"

    return HttpResponse(texto)


def detail(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)

    texto = "<h1>Información del cliente</h1>"
    texto += f"<p>Nombre: {cliente.nombre}</p>"
    texto += f"<p>Edad: {cliente.edad} años</p>"

    return HttpResponse(texto)