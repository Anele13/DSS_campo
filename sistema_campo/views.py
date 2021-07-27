from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from usuario.views import get_persona_campo
from campo.models import Campo

CANT_ANIMALES_HA = 15


def devolver_hacienda(request):

    campo = Campo.objects.get(persona=request.user.persona)
    datos_produccion = campo.datos_produccion_set.all()
    ultimo_registro = datos_produccion.order_by('-periodo')[0]
    return ultimo_registro.cantidad_ovejas, ultimo_registro.cantidad_carneros, ultimo_registro.cantidad_corderos, ultimo_registro.cantidad_muertes_corderos


def calcular_ocupacion(request):
    campo = Campo.objects.get(persona=request.user.persona)
    datos_produccion = campo.datos_produccion_set.all()
    ultimo_registro = datos_produccion.order_by('-periodo')[0]

    animales_ideales = campo.cant_hectareas * CANT_ANIMALES_HA
    animales_reales = ultimo_registro.cantidad_corderos + \
        ultimo_registro.cantidad_ovejas+ultimo_registro.cantidad_carneros

    cantidad_ha_ocupadas = round(animales_reales/CANT_ANIMALES_HA)
    cantidad_ha_reales = campo.cant_hectareas
    cantidad_ha_libres = cantidad_ha_reales-cantidad_ha_ocupadas

    return cantidad_ha_ocupadas, cantidad_ha_libres


@login_required(login_url='login')
def inicio(request):
    """
    Vista Inicio
    """
    resultado = {}
    produccion = {}
    contexto = {}
    user = request.user
    persona, campo = get_persona_campo(user)

    if not (persona and campo):
        messages.warning(request, "Cargue sus datos personales y de su campo.")

    elif not(campo.sonda):
        messages.warning(
            request, "Debe cargar los datos climaticos de su campo.")

    elif not(campo.datos_produccion_set.all()):
        messages.warning(
            request, "Debe cargar los datos de produccion de su campo.")

    else:
        cantidad_ovejas, cantidad_carneros, cantidad_corderos, mortandad = devolver_hacienda(
            request)
        ha_ocupadas, ha_libres = calcular_ocupacion(request)
        contexto = {'cantidad_ovejas': cantidad_ovejas, 'cantidad_carneros': cantidad_carneros,
                    'cantidad_corderos': cantidad_corderos, 'mortandad': mortandad, 'ha_ocupadas': ha_ocupadas, 'ha_libres': ha_libres}
    return render(request, "bienvenido.html", contexto)


@login_required(login_url='login')
def politica(request):
    """
    Vista Politicas de privacidad
    """
    return render(request, "politica_privacidad.html")
