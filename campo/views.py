from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from .models import Campo
from usuario.models import User
from django.db.models import Max
from django.db.models.functions import ExtractMonth, ExtractDay
import calendar
import locale
import statistics
import random


def get_mejor_año_por_condicion(query, datos_produccion, datos_climaticos):

    if query == 'rinde':
        max_rinde = datos_produccion.aggregate(Max('rinde_lana'))[
            'rinde_lana__max']
        mejor_año_rinde = datos_produccion.filter(
            rinde_lana=max_rinde)[0].periodo.year
        return mejor_año_rinde

    if query == 'finura':
        max_finura = datos_produccion.aggregate(Max('finura_lana'))[
            'finura_lana__max']
        mejor_año_finura = datos_produccion.filter(
            finura_lana=max_finura)[0].periodo.year
        return mejor_año_finura

    if query == 'lluvia':
        max_lluvia = datos_climaticos.aggregate(
            Max('mm_lluvia'))['mm_lluvia__max']
        mejor_año_lluvia = datos_climaticos.filter(
            mm_lluvia=max_lluvia)[0].periodo.year
        return mejor_año_lluvia

    if query == 'temperatura':
        max_temperatura = datos_climaticos.aggregate(Max('temperatura_maxima'))[
            'temperatura_maxima__max']
        mejor_año_temperatura = datos_climaticos.filter(
            temperatura_maxima=max_temperatura)[0].periodo.year
        return mejor_año_temperatura

    if query == 'mortandad':
        max_mortandad = datos_produccion.aggregate(Max('cantidad_muertes_corderos'))[
            'cantidad_muertes_corderos__max']
        max_año_mortandad = datos_produccion.filter(
            cantidad_muertes_corderos=max_mortandad)[0].periodo.year
        return max_año_mortandad

    if query == 'lana':
        max_lana = datos_produccion.aggregate(Max('cantidad_lana_producida'))[
            'cantidad_lana_producida__max']
        mejor_año_lana = datos_produccion.filter(
            cantidad_lana_producida=max_lana)[0].periodo.year
        return mejor_año_lana

    if query == 'carne':
        max_carne = datos_produccion.aggregate(Max('cantidad_carne_producida'))[
            'cantidad_carne_producida__max']
        mejor_año_carne = datos_produccion.filter(
            cantidad_carne_producida=max_carne)[0].periodo.year
        return datos_climaticos.filter(periodo__year=mejor_año_carne)

    if query == 'pariciones':
        max_cantidad_pariciones = datos_produccion.aggregate(
            Max('cantidad_pariciones'))['cantidad_pariciones__max']
        mejor_año_pariciones = datos_produccion.filter(
            cantidad_pariciones=max_cantidad_pariciones)[0].periodo.year
        return mejor_año_pariciones

    if query == 'hacienda':
        max_hacienda = datos_produccion.aggregate(Max('cantidad_ovejas'))[
            'cantidad_ovejas__max']
        mejor_año_hacienda = datos_produccion.filter(
            cantidad_ovejas=max_hacienda)[0].periodo.year
        return mejor_año_hacienda


@login_required(login_url='login')
# TODO probar otro default. la primera vez que solicita la pagina ya podria filtrar por alguna condicion
def mi_campo(request, query='rinde'):
    campo = Campo.objects.get(persona=request.user.persona)
    datos_produccion = campo.datos_produccion_set.all()
    datos_climaticos = campo.sonda.datos_climaticos_set.all()

    mejor_año = get_mejor_año_por_condicion(query, datos_produccion, datos_climaticos)
    datos_climaticos = datos_climaticos.filter(periodo__year=mejor_año).order_by('periodo')
    datos_produccion = datos_produccion.filter(periodo__year=mejor_año).order_by('periodo')

    resultado = {}
    produccion = {}
    meses = sorted(
        datos_climaticos
        .annotate(month=ExtractMonth('periodo'))
        .values_list('month', flat=True)
        .distinct()
    )

    
    datos = datos_climaticos.filter(periodo__month__gte=1, periodo__month__lte=12)
    datos_prod = datos_produccion.filter(periodo__month__gte=1, periodo__month__lte=12)
    d_1 = datos.values('periodo__month','temperatura_minima','mm_lluvia','temperatura_media','temperatura_maxima','velocidad_max_viento','humedad', 'periodo__day')
    d_2 = datos_prod.values('periodo__month','cantidad_ovejas','cantidad_corderos','cantidad_carneros','cantidad_lana_producida','cantidad_carne_producida')
    
    for mes in meses:  # dejo solo los meses que tengan datos
        d2 = list(filter(lambda d: d['periodo__month'] == mes, d_1))
        nombre_mes = calendar.month_name[mes]
        resultado[nombre_mes] = {'dias': [d['periodo__day'] for d in d2],
                                'temperatura_minima': min([d['temperatura_minima'] for d in d2]),
                                'lluvia': [d['mm_lluvia'] for d in d2],
                                'temperatura': [d['temperatura_media'] for d in d2],
                                'temperatura_maxima': max([d['temperatura_maxima'] for d in d2]),
                                'viento_promedio': statistics.mean([d['velocidad_max_viento'] for d in d2]),
                                'humedad_promedio': statistics.mean([d['humedad'] for d in d2])}
        d3 = list(filter(lambda d: d['periodo__month'] == mes, d_2))
        resultado[nombre_mes]['cant_ovejas'] = sum([d['cantidad_ovejas'] for d in d3])
        resultado[nombre_mes]['cant_corderos'] = sum([d['cantidad_corderos'] for d in d3])
        resultado[nombre_mes]['cant_carneros'] = sum([d['cantidad_carneros'] for d in d3])
    
    contexto = {}
    #contexto['meses'] = json.dumps([calendar.month_name[mes] for mes in  range(1,11)])
    contexto['lana'] = json.dumps([random.randint(600,800) for i in range(1,13)])#[d['cantidad_lana_producida'] for d in d3] TODO aca tambien va sum
    contexto['carne'] =  json.dumps([random.randint(30,50) for i in range(1,13)]) # [d['cantidad_carne_producida'] for d in d3]
    contexto['resultado'] = resultado
    contexto['año'] = mejor_año
    contexto['query'] = query
    return render(request, "mi_campo.html", contexto)
