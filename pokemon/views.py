from django.shortcuts import render
from django.http import Http404
import requests


def index(request):
    respuesta = requests.get(
        "https://microservicio-pokemon.onrender.com/pokemon"
    )

    pokemones = respuesta.json()

    context = {
        "pokemones": pokemones
    }

    return render(request, "pokemon/index.html", context)


def detalle(request, nombre):
    respuesta = requests.get(
        f"https://microservicio-pokemon.onrender.com/pokemon/{nombre}"
    )

    if respuesta.status_code == 404:
        raise Http404("Pokemon no encontrado")

    pokemon = respuesta.json()

    context = {
        "pokemon": pokemon
    }

    return render(request, "pokemon/detalle.html", context)