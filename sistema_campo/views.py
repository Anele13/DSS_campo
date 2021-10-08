from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from usuario.views import get_persona_campo
from django.contrib import messages
from campo.models import Campo

import calendar
import json

CANT_ANIMALES_HA = 15

def get_nombre_mes(numero_mes):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
             'Diciembre']
    return meses[numero_mes-1]

def devolver_hacienda(datos_produccion):

    ultimo_registro = datos_produccion.order_by('-periodo')[0]
    return ultimo_registro.cantidad_ovejas, ultimo_registro.cantidad_carneros, ultimo_registro.cantidad_corderos, ultimo_registro.cantidad_muertes_corderos


def calcular_ocupacion(campo, datos_produccion):

    ultimo_registro = datos_produccion.order_by('-periodo')[0]

    animales_ideales = campo.cant_hectareas * CANT_ANIMALES_HA
    animales_reales = ultimo_registro.cantidad_corderos + \
        ultimo_registro.cantidad_ovejas+ultimo_registro.cantidad_carneros

    cantidad_ha_excedida = 0
    cantidad_ha_ocupadas = round(animales_reales/CANT_ANIMALES_HA)
    cantidad_ha_reales = campo.cant_hectareas
    cantidad_ha_libres = cantidad_ha_reales-cantidad_ha_ocupadas
    if cantidad_ha_libres < 0:
        cantidad_ha_excedida = abs(cantidad_ha_libres)
        cantidad_ha_libres = 0

    return cantidad_ha_ocupadas, cantidad_ha_libres, cantidad_ha_excedida


def devolver_lluvias_mensuales(campo, datos_produccion, datos_climaticos):

    nombres_meses = []
    lluvias_mensuales = []

    anio_actual = datos_produccion.values(
        'periodo__year').order_by('-periodo')[0]['periodo__year']
    datos_climaticos_anio_actual = datos_climaticos.filter(
        periodo__year=anio_actual).order_by('periodo')
    datos_climaticos_meses = sorted(datos_climaticos_anio_actual.annotate(month=ExtractMonth(
        'periodo')).values_list('month', flat=True).distinct())

    d_1 = datos_climaticos_anio_actual.values('periodo__month', 'mm_lluvia',)

    for mes in list(set(datos_climaticos_meses)):
        d2 = list(filter(lambda d: d['periodo__month'] == mes, d_1))
        nombres_meses.append(get_nombre_mes(mes))
        lluvia_acumulada = round(sum([d['mm_lluvia'] for d in d2]), 2)
        lluvias_mensuales.append(lluvia_acumulada)

    join = list(zip(nombres_meses, lluvias_mensuales))
    join.sort(key=lambda tup: tup[1], reverse=True)
    lluvias_mensuales = [tup[1] for tup in join]
    nombres_meses = [tup[0] for tup in join]

    return nombres_meses, lluvias_mensuales


@login_required(login_url='login')
def inicio(request):
    """
    Vista Inicio
    """
    contexto = {}
    user = request.user
    persona, campo = get_persona_campo(user)

    if not (persona and campo):
        messages.warning(request, "Cargue sus datos personales y de su campo.")

    elif not(campo.sonda):
        messages.warning(
            request, "Debe cargar los datos climáticos de su campo.")

    elif not(campo.datos_produccion_set.all()):
        messages.warning(
            request, "Debe cargar los datos de producción de su campo.")

    else:

        campo = Campo.objects.get(persona=request.user.persona)
        datos_climaticos = campo.sonda.datos_climaticos_set.all()
        datos_produccion = campo.datos_produccion_set.all()

        cantidad_ovejas, cantidad_carneros, cantidad_corderos, mortandad = devolver_hacienda(
            datos_produccion)
        ha_ocupadas, ha_libres, ha_excedidas = calcular_ocupacion(
            campo, datos_produccion)
        nombres_meses, lluvias_mensuales = devolver_lluvias_mensuales(
            campo, datos_produccion, datos_climaticos)

        contexto = {'cantidad_ovejas': cantidad_ovejas, 'cantidad_carneros': cantidad_carneros,
                    'cantidad_corderos': cantidad_corderos, 'mortandad': mortandad, 'ha_ocupadas': ha_ocupadas,
                    'ha_libres': ha_libres, 'ha_excedidas': ha_excedidas, 'nombres_meses': json.dumps(nombres_meses), 'lluvias_mensuales': json.dumps(lluvias_mensuales)}
    return render(request, "bienvenido.html", contexto)