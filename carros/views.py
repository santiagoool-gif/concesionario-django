from django.shortcuts import render, get_object_or_404
from .models import Carro, Caracteristica
import requests


def index(request):
    latest_carro_list = Carro.objects.order_by("-pub_date")[:4]

    context = {
        "latest_carro_list": latest_carro_list,
    }

    return render(request, "carros/index.html", context)


def detail(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)

    context = {
        "carro": carro,
    }

    return render(request, "carros/detail.html", context)


def results(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)
    caracteristicas = carro.caracteristica_set.all()

    context = {
        "carro": carro,
        "caracteristicas": caracteristicas,
    }

    return render(request, "carros/results.html", context)


def comprar(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)

    context = {
        "carro": carro,
    }

    return render(request, "carros/detail.html", context)


def carros_nube(request):
    respuesta = requests.get("https://microservicio-carros.onrender.com/carros")
    carros = respuesta.json()
    context = {"carros": carros}
    return render(request, "carros/nube.html", context)