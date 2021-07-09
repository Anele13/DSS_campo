from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from .models import Campo
from django.db.models import Max
from django.db.models.functions import ExtractMonth, ExtractDay
import calendar, locale
import statistics

def get_mejor_año_por_condicion(query, datos_produccion,datos_climaticos):
    
    if query == 'rinde':   
        max_rinde = datos_produccion.aggregate(Max('rinde_lana'))['rinde_lana__max']
        mejor_año_rinde = datos_produccion.filter(rinde_lana=max_rinde)[0].periodo.year
        return mejor_año_rinde
    
    if query == 'finura':
        max_finura = datos_produccion.aggregate(Max('finura_lana'))['finura_lana__max']
        mejor_año_finura = datos_produccion.filter(finura_lana=max_finura)[0].periodo.year
        return mejor_año_finura
   
    if query == 'lluvia':
        max_lluvia = datos_climaticos.aggregate(Max('mm_lluvia'))['mm_lluvia__max']
        mejor_año_lluvia = datos_climaticos.filter(mm_lluvia=max_lluvia)[0].periodo.year
        return mejor_año_lluvia

    if query == 'temperatura':
        max_temperatura = datos_climaticos.aggregate(Max('temperatura_maxima'))['temperatura_maxima__max']
        mejor_año_temperatura = datos_climaticos.filter(temperatura_maxima=max_temperatura)[0].periodo.year
        return mejor_año_temperatura
    

    if query == 'mortandad':
        max_mortandad = datos_produccion.aggregate(Max('cantidad_muertes_corderos'))['cantidad_muertes_corderos__max']
        max_año_mortandad = datos_produccion.filter(cantidad_muertes_corderos=max_mortandad)[0].periodo.year
        return max_año_mortandad

    if query == 'lana':
        max_lana = datos_produccion.aggregate(Max('cantidad_lana_producida'))['cantidad_lana_producida__max']
        mejor_año_lana = datos_produccion.filter(cantidad_lana_producida=max_lana)[0].periodo.year
        return mejor_año_lana
    
    if query == 'carne':
        max_carne = datos_produccion.aggregate(Max('cantidad_carne_producida'))['cantidad_carne_producida__max']
        mejor_año_carne = datos_produccion.filter(cantidad_carne_producida=max_carne)[0].periodo.year
        return datos_climaticos.filter(periodo__year=mejor_año_carne)

    
    if query == 'pariciones':
        max_cantidad_pariciones = datos_produccion.aggregate(Max('cantidad_pariciones'))['cantidad_pariciones__max']
        mejor_año_pariciones = datos_produccion.filter(cantidad_pariciones=max_cantidad_pariciones)[0].periodo.year
        return mejor_año_pariciones
    
    if query == 'hacienda':
        max_hacienda = datos_produccion.aggregate(Max('cantidad_ovejas'))['cantidad_ovejas__max']
        mejor_año_hacienda = datos_produccion.filter(cantidad_ovejas=max_hacienda)[0].periodo.year
        return mejor_año_hacienda


@login_required(login_url='login')
def mi_campo(request, query='rinde'): #TODO probar otro default. la primera vez que solicita la pagina ya podria filtrar por alguna condicion
    campo = Campo.objects.get(persona=request.user.persona)
    datos_produccion = campo.datos_produccion_set.all()
    datos_climaticos = campo.sonda.datos_climaticos_set.all()

    mejor_año = get_mejor_año_por_condicion(query, datos_produccion, datos_climaticos)
    datos_climaticos = datos_climaticos.filter(periodo__year=mejor_año).order_by('periodo')
    datos_produccion =  datos_produccion.filter(periodo__year=mejor_año).order_by('periodo')

    resultado={}
    meses = sorted(
        datos_climaticos
        .annotate(month=ExtractMonth('periodo'))
        .values_list('month', flat=True)
        .distinct()
    )

    for mes in meses: #dejo solo los meses que tengan datos
        datos = datos_climaticos.filter(periodo__month__gte=mes, periodo__month__lte=mes)
        dias = datos.annotate(day=ExtractDay('periodo')).values_list('day', flat=True).distinct()
        resultado[calendar.month_name[mes]] = {'dias': list(dias),
                                                'temperatura_minima': min(list(datos.values_list('temperatura_media',flat=True))),
                                                'lluvia': list(datos.values_list('mm_lluvia',flat=True)),
                                                'temperatura': list(datos.values_list('temperatura_media',flat=True)),
                                                'temperatura_maxima': max(list(datos.values_list('temperatura_media',flat=True))),
                                                'viento_promedio': statistics.mean(list(datos.values_list('velocidad_max_viento',flat=True))),
                                                'humedad_promedio': statistics.mean(list(datos.values_list('humedad',flat=True)))}

    contexto={}
    contexto['resultado'] = resultado
    contexto['año'] = mejor_año
    return render(request, "mi_campo.html", contexto)