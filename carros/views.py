from django.shortcuts import render, get_object_or_404
from .models import Carro, Caracteristica
import requests
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

def carros_por_anio(request, anio):
    respuesta = requests.get(
        f"https://microservicio-carros.onrender.com/carros/{anio}"
    )

    carros = respuesta.json()

    context = {
        "carros": carros
    }

    return render(request, "carros/nube.html", context)

def ia_concesionario(request):
    respuesta_ia = ""

    if request.method == "POST":
        pregunta = request.POST.get("pregunta")

        if pregunta:
            response = client.models.generate_content(
               model="gemini-3.5-flash-lite",
                contents=f"""
                Eres un asistente virtual de un concesionario de vehículos.
                Responde preguntas relacionadas con carros, características,
                mantenimiento, compra, venta y funcionamiento de vehículos.

                Pregunta del usuario:
                {pregunta}
                """
            )

            respuesta_ia = response.text

    return render(
        request,
        "carros/asistente.html",
        {"respuesta_ia": respuesta_ia}
    )