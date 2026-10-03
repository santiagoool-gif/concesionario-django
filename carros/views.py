from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Carro, Caracteristica
from .forms import CarroForm, CaracteristicaForm

import os
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()



client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "dev-internal-token")
CARROS_API_URL = os.getenv(
    "CARROS_API_URL",
    "http://127.0.0.1:8000/carros/api/carros/",
)
NODE_INSERT_URL = os.getenv("NODE_INSERT_URL", "").rstrip("/")
NODE_UPDATE_URL = os.getenv("NODE_UPDATE_URL", "").rstrip("/")
NODE_DELETE_URL = os.getenv("NODE_DELETE_URL", "").rstrip("/")
READ_PRIMARY_URL = os.getenv("READ_PRIMARY_URL", "").rstrip("/")
READ_FALLBACK_URL = os.getenv("READ_FALLBACK_URL", "").rstrip("/")


def _headers_internos():
    return {"X-Internal-Token": INTERNAL_API_TOKEN}


def _usar_microservicio(url):
    return bool(url)



# PRIMERAS 


def index(request):
    latest_carro_list = Carro.objects.order_by("-pub_date")[:4]
    return render(request, "carros/index.html", {
        "latest_carro_list": latest_carro_list,
    })


def detail(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)
    return render(request, "carros/detail.html", {"carro": carro})


def results(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)
    caracteristicas = carro.caracteristica_set.all()
    return render(request, "carros/results.html", {
        "carro": carro,
        "caracteristicas": caracteristicas,
        
    })



# CRUD - LAS OPERACIONES PUEDEN PASAR POR NODE.JS


def crear_carro(request):
    if request.method == "POST":
        form = CarroForm(request.POST)
        if form.is_valid():
            if _usar_microservicio(NODE_INSERT_URL):
                data = form.cleaned_data
                try:
                    response = requests.post(
                        f"{NODE_INSERT_URL}/carros",
                        json={
                            "carro_text": data["carro_text"],
                            "precio": str(data["precio"]),
                            "pub_date": data["pub_date"].isoformat(),
                            "año": data["carro_text"],
                        },
                        timeout=10,
                    )
                    response.raise_for_status()
                except requests.RequestException:
                    form.add_error(None, "No fue posible comunicarse con el microservicio de inserción.")
                    return render(request, "carros/form.html", {
                        "form": form,
                        "titulo": "Registrar nuevo carro",
                        "boton": "Guardar carro",
                    })
            else:
                form.save()
            return redirect("carros:index")
    else:
        form = CarroForm()

    return render(request, "carros/form.html", {
        "form": form,
        "titulo": "Registrar nuevo carro",
        "boton": "Guardar carro",
    })


def editar_carro(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)

    if request.method == "POST":
        form = CarroForm(request.POST, instance=carro)
        if form.is_valid():
            if _usar_microservicio(NODE_UPDATE_URL):
                data = form.cleaned_data
                try:
                    response = requests.put(
                        f"{NODE_UPDATE_URL}/carros/{carro.id}",
                        json={
                            "carro_text": data["carro_text"],
                            "precio": str(data["precio"]),
                            "pub_date": data["pub_date"].isoformat(),
                        },
                        timeout=10,
                    )
                    response.raise_for_status()
                except requests.RequestException:
                    form.add_error(None, "No fue posible comunicarse con el microservicio de actualización.")
                    return render(request, "carros/form.html", {
                        "form": form,
                        "titulo": "Editar carro",
                        "boton": "Guardar cambios",
                        "carro": carro,
                    })
            else:
                form.save()
            return redirect("carros:detail", carro_id=carro.id)
    else:
        form = CarroForm(instance=carro)

    return render(request, "carros/form.html", {
        "form": form,
        "titulo": "Editar carro",
        "boton": "Guardar cambios",
        "carro": carro,
    })


def eliminar_carro(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)

    if request.method == "POST":
        if _usar_microservicio(NODE_DELETE_URL):
            try:
                response = requests.delete(
                    f"{NODE_DELETE_URL}/carros/{carro.id}",
                    timeout=10,
                )
                response.raise_for_status()
            except requests.RequestException:
                return HttpResponse(
                    "No fue posible comunicarse con el microservicio de eliminación.",
                    status=502,
                )
        else:
            carro.delete()
        return redirect("carros:index")

    return render(request, "carros/confirmar_eliminar.html", {"carro": carro})


# OTRAS VISTAS


def comprar(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)
    return render(request, "carros/comprar.html", {"carro": carro})


def carros_nube(request):
    try:
        response = requests.get(
            "https://microservicio-carros.onrender.com/carros",
            timeout=10,
        )
        response.raise_for_status()
        carros = response.json()
    except requests.RequestException:
        carros = []

    return render(request, "carros/nube.html", {"carros": carros})


def carros_por_anio(request, anio):
    carros = Carro.objects.filter(pub_date__year=anio).order_by("-pub_date")
    return render(request, "carros/index.html", {
        "carros": carros,
        "anio": anio,
        "latest_carro_list": carros,
    })



# API PUBLICA DE DATOS


def _datos_carros():
    carros = Carro.objects.all().order_by("-pub_date")
    datos = []

    for carro in carros:
        datos.append({
            "id": carro.id,
            "nombre": carro.carro_text,
            "precio": str(carro.precio),
            "fecha_publicacion": carro.pub_date.strftime("%Y-%m-%d"),
            "caracteristicas": list(
                carro.caracteristica_set.values_list(
                    "caracteristica_text", flat=True
                )
            ),
        })

    return datos


def api_carros(request):
    return JsonResponse(_datos_carros(), safe=False)


def api_carros_resiliente(request):
    """Consulta un microservicio Node y usa otro como respaldo."""
    urls = [READ_PRIMARY_URL, READ_FALLBACK_URL]

    for url in urls:
        if not url:
            continue
        try:
            response = requests.get(f"{url}/carros", timeout=5)
            response.raise_for_status()
            return JsonResponse({
                "fuente": url,
                "resiliencia": "principal_o_respaldo",
                "carros": response.json(),
            })
        except requests.RequestException:
            continue

    # Ultimo respaldo: base de datos local de Django.
    return JsonResponse({
        "fuente": "django-db",
        "resiliencia": "respaldo_final",
        "carros": _datos_carros(),
    })



# API INTERNA PARA LOS MICROSERVICIOS NODE.JS


def _token_valido(request):
    return request.headers.get("X-Internal-Token") == INTERNAL_API_TOKEN


@csrf_exempt
def api_interno_crear(request):
    if not _token_valido(request):
        return JsonResponse({"error": "No autorizado"}, status=401)
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    try:
        import json
        data = json.loads(request.body or "{}")
        carro = Carro.objects.create(
            carro_text=data["carro_text"],
            precio=data["precio"],
            pub_date=parse_datetime(data["pub_date"]) if isinstance(data.get("pub_date"), str) else data["pub_date"],
        )
        return JsonResponse({"id": carro.id, "mensaje": "Carro creado"}, status=201)
    except (KeyError, ValueError, TypeError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)


@csrf_exempt
def api_interno_actualizar(request, carro_id):
    if not _token_valido(request):
        return JsonResponse({"error": "No autorizado"}, status=401)
    if request.method != "PUT":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    carro = get_object_or_404(Carro, pk=carro_id)
    try:
        import json
        data = json.loads(request.body or "{}")
        carro.carro_text = data.get("carro_text", carro.carro_text)
        carro.precio = data.get("precio", carro.precio)
        if data.get("pub_date"):
            carro.pub_date = parse_datetime(data["pub_date"])
        carro.save()
        return JsonResponse({"id": carro.id, "mensaje": "Carro actualizado"})
    except (ValueError, TypeError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)


@csrf_exempt
def api_interno_eliminar(request, carro_id):
    if not _token_valido(request):
        return JsonResponse({"error": "No autorizado"}, status=401)
    if request.method != "DELETE":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    carro = get_object_or_404(Carro, pk=carro_id)
    carro.delete()
    return JsonResponse({"mensaje": "Carro eliminado", "id": carro_id})



# CARACTERISTICAS


def agregar_caracteristica(request, carro_id):
    carro = get_object_or_404(Carro, pk=carro_id)
    if request.method == "POST":
        caracteristica_text = request.POST.get("caracteristica_text", "").strip()
        if caracteristica_text:
            Caracteristica.objects.create(
                carro=carro,
                caracteristica_text=caracteristica_text,
            )
        return redirect("carros:detail", carro_id=carro.id)

    return render(request, "carros/agregar_caracteristica.html", {"carro": carro})


def editar_caracteristica(request, caracteristica_id):
    caracteristica = get_object_or_404(Caracteristica, pk=caracteristica_id)
    if request.method == "POST":
        form = CaracteristicaForm(request.POST, instance=caracteristica)
        if form.is_valid():
            form.save()
            return redirect("carros:detail", carro_id=caracteristica.carro.id)
    else:
        form = CaracteristicaForm(instance=caracteristica)

    return render(request, "carros/caracteristica_form.html", {
        "form": form,
        "caracteristica": caracteristica,
    })


def eliminar_caracteristica(request, caracteristica_id):
    caracteristica = get_object_or_404(Caracteristica, pk=caracteristica_id)
    carro_id = caracteristica.carro.id
    if request.method == "POST":
        caracteristica.delete()
        return redirect("carros:detail", carro_id=carro_id)

    return render(request, "carros/confirmar_eliminar_caracteristica.html", {
        "caracteristica": caracteristica,
    })


# ASISTENTE IA


def ia_concesionario(request):
    respuesta = None
    pregunta = ""
    fuente_datos = CARROS_API_URL

    if request.method == "POST":
        pregunta = request.POST.get("pregunta", "").strip()

        if pregunta:
            # 1. Consultar el inventario
            try:
                api_response = requests.get(
                    CARROS_API_URL,
                    timeout=8
                )
                api_response.raise_for_status()
                informacion_carros = api_response.json()

            except requests.RequestException:
                informacion_carros = _datos_carros()
                fuente_datos = "respaldo-local-django"

            # 2. Preparar la información para la IA
            contexto = f"""
Eres el asistente virtual de un concesionario de vehículos.

Usa exclusivamente los datos del inventario proporcionado a continuación
para responder preguntas sobre vehículos, precios y características.

No inventes precios ni características.

INVENTARIO ACTUAL:
{informacion_carros}

PREGUNTA DEL USUARIO:
{pregunta}

Responde en español de forma clara, útil y profesional.

Si el vehículo o dato solicitado no aparece en el inventario,
dilo claramente.
"""

            # 3. Intentar diferentes modelos de IA
            modelos = [
                GEMINI_MODEL,
                "gemini-3.7-flash",
                "gemini-3.5-flash",
            ]

            respuesta = None

            for modelo in modelos:
                try:
                    response = client.models.generate_content(
                        model=modelo,
                        contents=contexto,
                    )

                    respuesta = response.text
                    break

                except Exception:
                    continue

            # 4. Si todos los modelos fallan
            if respuesta is None:
                respuesta = (
                    "La inteligencia artificial está temporalmente "
                    "saturada. Intenta nuevamente en unos segundos."
                )

    return render(
        request,
        "carros/asistente.html",
        {
            "respuesta": respuesta,
            "pregunta": pregunta,
            "fuente_datos": fuente_datos,
        }
    )


# VISTAS GENERICAS DE DJANGO


class CarroListView(ListView):
    model = Carro
    template_name = "carros/index.html"
    context_object_name = "latest_carro_list"
    ordering = ["-pub_date"]


class CarroDetailView(DetailView):
    model = Carro
    template_name = "carros/detail.html"
    context_object_name = "carro"


class CarroCreateView(CreateView):
    model = Carro
    form_class = CarroForm
    template_name = "carros/form.html"
    success_url = reverse_lazy("carros:index")


class CarroUpdateView(UpdateView):
    model = Carro
    form_class = CarroForm
    template_name = "carros/form.html"
    success_url = reverse_lazy("carros:index")


class CarroDeleteView(DeleteView):
    model = Carro
    template_name = "carros/confirmar_eliminar.html"
    success_url = reverse_lazy("carros:index")
