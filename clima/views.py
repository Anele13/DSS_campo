from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import pandas as pd
from .models import DatosClimaticos, Sonda
from campo.models import Campo
from usuario.models import Persona
from usuario.views import get_persona_campo


@login_required(login_url='login')
def cargar_datos_climaticos(request):
    contexto = {}
    user = request.user
    if request.method == 'POST':
        try:
            campo = Campo.objects.get(persona=user.persona)
            if 'archivo_csv' in request.FILES:
                archivo_climatico = request.FILES['archivo_csv']
                campo.get_or_create_sonda().agregar_datos_climaticos(archivo_climatico)
                messages.success(request, "Datos registrados exitosamente")
            else:
                latitud = request.POST.get('latitud')
                longitud = request.POST.get('longitud')
                sonda = Sonda.objects.get(latitud=latitud, longitud=longitud)
                campo.sonda = sonda
                campo.save()
                sondas = Sonda.objects.filter(pertenencia='INTA')
                contexto['sondas'] = Sonda.formatear(sondas)
                messages.success(request, "Sonda cargada exitosamente")
        except Exception as e:
            messages.warning(request,str(e))
    else:
        persona, campo = get_persona_campo(user)
        if not (persona and campo):
            messages.warning(request, "Cargue sus datos personales y de su campo.")
        else:
            sondas = Sonda.objects.filter(pertenencia='INTA')
            contexto['sondas'] = Sonda.formatear(sondas)
    return render(request, "alta_datos_climaticos.html", contexto)
