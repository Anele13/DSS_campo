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
    ha_campo = campo.cant_hectareas
    animales_ideales = ha_campo * CANT_ANIMALES_HA
    diaria = campo.get_diaria_data()
    animales_reales = 0
    if diaria:
        animales_reales = sum([v for k, v in diaria.items() if k in ['carneros', 'corderos', 'ovejas']])

    hectareas_ocupadas = round(animales_reales / CANT_ANIMALES_HA)
    porcentaje_ha_libres = calcular_porcentaje_libre(animales_ideales, animales_reales)
    porcentaje_ha_ocupadas = 100 - porcentaje_ha_libres
    cantidad_ha_faltante = 0
    
    if porcentaje_ha_ocupadas >= 100:
        cantidad_ha_faltante = calcular_exceso(animales_ideales, animales_reales)
        porcentaje_ha_libres = 0
        porcentaje_ha_ocupadas = 100
    try:
        return round(porcentaje_ha_ocupadas,2), round(porcentaje_ha_libres,2), round(cantidad_ha_faltante,2), hectareas_ocupadas
    except:
        return 0,0,0

def devolver_lluvias_mensuales(campo=None):
    import locale
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
    nombres_meses = []
    lluvias_mensuales = []
    df = campo.get_firebase_data()
    if not df.empty and all(item in df.columns for item in ['periodo', 'mm_lluvia']):
        año_actual = df.periodo.max().year
        df = df[df.periodo.dt.year == año_actual].groupby(df.periodo.dt.month)['mm_lluvia'].sum().reset_index()
        df.periodo = df.periodo.apply(lambda mes: datetime.strptime(str(mes), '%m').strftime("%B").capitalize())
        nombres_meses = df.periodo.to_list()
        lluvias_mensuales = df.mm_lluvia.to_list()
    return nombres_meses, lluvias_mensuales


@login_required(login_url='login')
def inicio(request):
    """
    Vista Inicio
    """
    campo = Campo.objects.get(persona=request.user.persona)
    datos_climaticos = campo.clima_actual()
    porc_ha_ocupadas, porc_ha_libres, ha_excedidas, hectareas_ocupadas = calcular_ocupacion_campo(campo)
    nombres_meses, lluvias_mensuales = devolver_lluvias_mensuales(campo)
    hectareas_libres = campo.cant_hectareas - hectareas_ocupadas
    hectareas_libres = hectareas_libres if hectareas_libres >=0 else 0
    contexto={
        'campo_id': campo.id, 
        'localidad': datos_climaticos.get('localidad'),
        'temperatura': datos_climaticos.get('temperatura'),
        'viento': datos_climaticos.get('velocidad_viento'),
        'humedad': datos_climaticos.get('humedad'),
        'timestamp': str(datetime.now().strftime('%H:%M')),
        'porc_ha_ocupadas': porc_ha_ocupadas,
        'porc_ha_libres': porc_ha_libres, 
        'ha_excedidas': ha_excedidas,
        'hectareas_ocupadas': hectareas_ocupadas,
        'hectareas_ocupadas': hectareas_ocupadas,
        'hectareas_libres': hectareas_libres,
        'campo': campo,
        'nombres_meses': json.dumps(nombres_meses),
        'lluvias_mensuales': lluvias_mensuales,
    }
    #print(datos_climaticos)
    return render(request, "bienvenido.html", contexto)