from django.http import HttpResponse
from .models import Carro, Caracteristica


def index(request):
    latest_carro_list = Carro.objects.order_by("-pub_date")[:4]

    texto = "<h1>Concesionario</h1>"
    texto += "<h2>Últimos carros registrados</h2>"

    for carro in latest_carro_list:
        texto += f"<p>🚗 {carro.carro_text}</p>"

    return HttpResponse(texto)


def detail(request, carro_id):
    carro = Carro.objects.get(pk=carro_id)
    return HttpResponse(f"Estás viendo el carro: {carro}")


def results(request, carro_id):
    carro = Carro.objects.get(pk=carro_id)
    caracteristicas = carro.caracteristica_set.all()

    texto = f"<h1>Resultados: {carro.carro_text}</h1>"

    for caracteristica in caracteristicas:
        texto += f"<p>{caracteristica.caracteristica_text} - Votos: {caracteristica.votos}</p>"

    return HttpResponse(texto)


def vote(request, carro_id):
    return HttpResponse(f"Estás votando por el carro {carro_id}.")