from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import pandas as pd
from .models import DatosClimaticos, Sonda
from campo.models import Campo


def formatear_sondas(sondas):
    respuesta = {}
    for s in sondas:
        if s.latitud and s.longitud:
            respuesta[str(s.id)] = {'nombre': s.nombre,
                                    'latitud': s.latitud,
                                    'longitud': s.longitud,
                                    'altura': 0}
    return json.dumps(respuesta)


@login_required(login_url='login')
def cargar_datos_climaticos(request):
    contexto = {}

    # TODO: mejorar esto, esta quedando un 1 en la base para las sondas que no son inta.
    sondas = Sonda.objects.filter(pertenencia='INTA')
    contexto['sondas'] = formatear_sondas(sondas)
    if request.method == 'POST':
        try:
            campo = Campo.objects.filter(persona=request.user.persona)
            if campo:
                if 'archivo_csv' in request.FILES:
                    archivo_climatico = request.FILES['archivo_csv']
                    try:
                        campo.get_or_create_sonda().agregar_datos_climaticos(archivo_climatico)
                        messages.success(
                            request, "Datos registrados exitosamente")
                    except Exception as e:
                        messages.warning(request, str(e))
                else:
                    latitud = request.POST.get('latitud')
                    longitud = request.POST.get('longitud')
                    sonda = Sonda.objects.get(
                        latitud=latitud, longitud=longitud)
                    campo.sonda = sonda
                    campo.save()
                    messages.success(request, "Sonda cargada exitosamente")
            else:
                messages.warning(
                    request, "Porfavor cargue los datos de su campo desde su perfil")
        except Exception as e2:
            messages.warning(
                request, "Porfavor cargue los datos personales y de su campo desde su perfil"+str(e2))
    return render(request, "alta_datos_climaticos.html", contexto)
