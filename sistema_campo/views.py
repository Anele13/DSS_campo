from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from usuario.views import get_persona_campo
from campo.models import Campo


def devolver_hacienda(request):
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
        campo = Campo.objects.get(persona=request.user.persona)
        datos_produccion = campo.datos_produccion_set.all()
        ultimo_registro = datos_produccion.order_by('-periodo')[0]
        return ultimo_registro.cantidad_ovejas, ultimo_registro.cantidad_carneros, ultimo_registro.cantidad_corderos, ultimo_registro.cantidad_muertes_corderos


@login_required(login_url='login')
def inicio(request):
    """
    Vista Inicio
    """
    resultado = {}
    produccion = {}
    contexto = {}
    cantidad_ovejas, cantidad_carneros, cantidad_corderos, mortandad = devolver_hacienda(
        request)
    contexto = {'cantidad_ovejas': cantidad_ovejas, 'cantidad_carneros': cantidad_carneros,
                'cantidad_corderos': cantidad_corderos, 'mortandad': mortandad}
    return render(request, "bienvenido.html", contexto)


@login_required(login_url='login')
def politica(request):
    """
    Vista Politicas de privacidad
    """
    return render(request, "politica_privacidad.html")
