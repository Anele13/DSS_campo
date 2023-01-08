from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from usuario.views import get_persona_campo
from django.contrib import messages
from campo.models import Campo
from datetime import datetime

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

def calcular_porcentaje_libre(animales_ideales, animales_reales):
  total_animales = animales_ideales - animales_reales
  porcentaje_ha_libres = total_animales/animales_ideales * 100
  return round(porcentaje_ha_libres,2)

def calcular_exceso(animales_ideales, animales_reales):
  total_animales = animales_ideales - animales_reales
  cantidad_ha_faltante = total_animales/CANT_ANIMALES_HA
  return round(abs(cantidad_ha_faltante))

def calcular_ocupacion_campo(campo):

    #ultimo_registro = datos_produccion.order_by('-periodo')[0]
    #animales_reales = ultimo_registro.cantidad_corderos + \
    #ultimo_registro.cantidad_ovejas+ultimo_registro.cantidad_carneros
    
    ha_campo = campo.cant_hectareas
    animales_ideales = ha_campo * CANT_ANIMALES_HA
    animales_reales = 5680
    porcentaje_ha_libres = calcular_porcentaje_libre(animales_ideales, animales_reales)
    porcentaje_ha_ocupadas = 100 - porcentaje_ha_libres
    cantidad_ha_faltante = 0
    
    if porcentaje_ha_ocupadas >= 100:
        cantidad_ha_faltante = calcular_exceso(animales_ideales, animales_reales)
        porcentaje_ha_libres = 0
        porcentaje_ha_ocupadas = 100

    return porcentaje_ha_ocupadas, porcentaje_ha_libres, cantidad_ha_faltante


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
    campo = Campo.objects.get(persona=request.user.persona)
    datos_climaticos = campo.clima_actual()
    ha_ocupadas, ha_libres, ha_excedidas = calcular_ocupacion_campo(campo)
    contexto={
        'campo_id': campo.id, 
        'localidad': datos_climaticos.get('localidad'),
        'temperatura': datos_climaticos.get('temperatura'),
        'viento': datos_climaticos.get('velocidad_viento'),
        'humedad': datos_climaticos.get('humedad'),
        'timestamp': str(datetime.now().strftime('%H:%M')),
        'ha_ocupadas': ha_ocupadas,
        'ha_libres': ha_libres, 
        'ha_excedidas': ha_excedidas,
    }
    #print(datos_climaticos)
    return render(request, "bienvenido.html", contexto)