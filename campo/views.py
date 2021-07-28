from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from .models import Campo
from usuario.models import User
from django.db.models import Max, Sum, Min
from django.db.models.functions import ExtractMonth, ExtractDay
from usuario.views import get_persona_campo
import calendar
import locale
import statistics
import random


def get_mejor_año_por_condicion(query, datos_produccion, datos_climaticos):

    # para el maximo valor es order by con el - adelante.

    if query == 'rinde':
        return datos_produccion.values('periodo__year').\
            annotate(rinde_anual=Max('rinde_lana')).\
            order_by('-rinde_anual')[0]['periodo__year']

    if query == 'finura':
        return datos_produccion.filter(finura_lana__gt=0).values('periodo__year').\
            annotate(finura_anual=Min('finura_lana')).\
            order_by('finura_anual')[0]['periodo__year']  # TODO checkaear

    if query == 'lluvia':
        return datos_climaticos.values('periodo__year').\
            annotate(mm_lluvia_anual=Sum('mm_lluvia')).\
            order_by('-mm_lluvia_anual')[0]['periodo__year']

    if query == 'temperatura':
        max_temperatura = datos_climaticos.aggregate(Max('temperatura_maxima'))[
            'temperatura_maxima__max']
        mejor_año_temperatura = datos_climaticos.filter(
            temperatura_maxima=max_temperatura)[0].periodo.year
        return mejor_año_temperatura

    if query == 'mortandad':
        return datos_produccion.values('periodo__year').\
            annotate(mortandad_anual=Sum('cantidad_muertes_corderos')).\
            order_by('mortandad_anual')[0]['periodo__year']

    if query == 'lana':
        return datos_produccion.values('periodo__year').\
            annotate(kg_lana_anual=Sum('cantidad_lana_producida')).\
            order_by('-kg_lana_anual')[0]['periodo__year']

    if query == 'carne':
        return datos_produccion.values('periodo__year').\
            annotate(kg_carne_anual=Sum('cantidad_carne_producida')).\
            order_by('-kg_carne_anual')[0]['periodo__year']

    if query == 'pariciones':
        return datos_produccion.values('periodo__year').\
            annotate(pariciones_anual=Sum('cantidad_pariciones')).\
            order_by('-pariciones_anual')[0]['periodo__year']

    if query == 'hacienda':
        return datos_produccion.values('periodo__year').\
            annotate(cantidad_ovejas_anual=Max('cantidad_ovejas')).\
            order_by('-cantidad_ovejas_anual')[0]['periodo__year']


@login_required(login_url='login')
def mi_campo(request, query='rinde'):
    user = request.user
    persona, campo = get_persona_campo(user)
    resultado = {}
    produccion = {}
    contexto = {}

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
        datos_climaticos = campo.sonda.datos_climaticos_set.all()

        mejor_año = get_mejor_año_por_condicion(
            query, datos_produccion, datos_climaticos)
        datos = datos_climaticos.filter(
            periodo__year=mejor_año).order_by('periodo')
        datos_prod = datos_produccion.filter(
            periodo__year=mejor_año).order_by('periodo')
        meses = sorted(datos.annotate(month=ExtractMonth(
            'periodo')).values_list('month', flat=True).distinct())

        d_1 = datos.values('periodo__month',
                           'temperatura_minima',
                           'mm_lluvia',
                           'temperatura_media',
                           'temperatura_maxima',
                           'velocidad_max_viento',
                           'humedad',
                           'periodo__day')

        d_2 = datos_prod.values('periodo__month',
                                'cantidad_ovejas',
                                'cantidad_corderos',
                                'cantidad_carneros',
                                'cantidad_lana_producida',
                                'cantidad_carne_producida',
                                'rinde_lana',
                                'finura_lana')

        # TODO chequear cuando no tenes datos que mandas!! por ejemplo los viento y humedad
        for mes in list(set(meses)):  # dejo solo los meses que tengan datos
            d2 = list(filter(lambda d: d['periodo__month'] == mes, d_1))
            nombre_mes = calendar.month_name[mes]
            resultado[nombre_mes] = {'dias': [d['periodo__day'] for d in d2],
                                     'temperatura_minima': min([d['temperatura_minima'] for d in d2]),
                                     'lluvia': [d['mm_lluvia'] for d in d2],
                                     'temperatura': [d['temperatura_media'] for d in d2],
                                     'temperatura_maxima': max([d['temperatura_maxima'] for d in d2]),
                                     # statistics.mean([d['velocidad_max_viento'] for d in d2]),
                                     'viento_promedio': 100,
                                     'humedad_promedio': 100}  # statistics.mean([d['humedad'] for d in d2])}

            d3 = list(filter(lambda d: d['periodo__month'] == mes, d_2))
            resultado[nombre_mes]['cant_ovejas'] = sum(
                [d['cantidad_ovejas'] for d in d3])
            resultado[nombre_mes]['cant_corderos'] = sum(
                [d['cantidad_corderos'] for d in d3])
            resultado[nombre_mes]['cant_carneros'] = sum(
                [d['cantidad_carneros'] for d in d3])

            # En rinde se busca el Max, finura el Min, Carne y Lana Buscas la suma mensual
            resultado[nombre_mes]['rinde_lana_meses'] = max([
                d['rinde_lana'] for d in d3])
            resultado[nombre_mes]['finura_lana_meses'] = min([
                d['finura_lana'] for d in d3])
            resultado[nombre_mes]['cant_carne_meses'] = sum([
                d['cantidad_carne_producida'] for d in d3])
            resultado[nombre_mes]['cant_lana_meses'] = sum([
                d['cantidad_lana_producida'] for d in d3])

        contexto['resultado'] = resultado
        contexto['año'] = mejor_año
        contexto['query'] = query
    return render(request, "mi_campo.html", contexto)
