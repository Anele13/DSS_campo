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
import pandas as pd
from datetime import datetime

import firebase_admin
from firebase_admin import db
if not firebase_admin._apps:
    DATABASE_URL = 'https://dss-campo-default-rtdb.firebaseio.com/'
    CREDENTIALS = 'dss-campo-firebase-adminsdk-3mpy4-19ac4df912.json'
    firebase_admin.initialize_app(firebase_admin.credentials.Certificate(CREDENTIALS), {'databaseURL':DATABASE_URL})


def get_nombre_mes(numero_mes):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre',
             'Diciembre']
    return meses[numero_mes-1]


def get_mejor_año_por_condicion(query, datos_produccion, datos_climaticos):
    # para el maximo valor es order by con el - adelante.
    mejor_año = 2010
    
    if query == 'rinde':
        datos_produccion.rinde_lana = datos_produccion.rinde_lana.astype(int)
        mejor_año = datos_produccion[['year','rinde_lana']].\
            groupby("year").\
            max().\
            reset_index().\
            sort_values(by=['rinde_lana'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    if query == 'finura':
        datos_produccion.finura_lana = datos_produccion.finura_lana.astype(int)
        mejor_año = datos_produccion[['year','finura_lana']].\
            groupby("year").\
            max().\
            reset_index().\
            sort_values(by=['finura_lana'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    if query == 'lluvia':
        datos_climaticos.mm_lluvia = datos_climaticos.mm_lluvia.astype(int)
        mejor_año = datos_climaticos[['year','mm_lluvia']].\
            groupby("year").\
            max().\
            reset_index().\
            sort_values(by=['mm_lluvia'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    if query == 'temperatura':
        datos_climaticos = datos_climaticos[datos_climaticos.month.isin([1,2,3])]
        datos_climaticos.temperatura_maxima = datos_climaticos.temperatura_maxima.astype(int)
        mejor_año = datos_climaticos[['year','temperatura_maxima']].\
            groupby("year").\
            max().\
            reset_index().\
            sort_values(by=['temperatura_maxima'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    if query == 'mortandad':
        datos_produccion.muertes = datos_produccion.muertes.astype(int)
        mejor_año = datos_produccion[['year','muertes']].\
            groupby("year").\
            sum().\
            reset_index().\
            sort_values(by=['muertes'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    if query == 'lana':
        datos_produccion.lana_producida = datos_produccion.lana_producida.astype(int)
        mejor_año = datos_produccion[['year','lana_producida']].\
            groupby("year").\
            sum().\
            reset_index().\
            sort_values(by=['lana_producida'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    """
    if query == 'carne':
        return datos_produccion.values('periodo__year').\
            annotate(kg_carne_anual=Sum('cantidad_carne_producida')).\
            order_by('-kg_carne_anual')[0]['periodo__year']
        
        datos_produccion.pariciones = datos_produccion.pariciones.astype(int)
        mejor_año = datos_produccion[['year','pariciones']].\
            groupby("year").\
            sum().\
            reset_index().\
            sort_values(by=['pariciones'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]
    """ #NO esta mas carne como variable 

    if query == 'pariciones':
        datos_produccion.pariciones = datos_produccion.pariciones.astype(int)
        mejor_año = datos_produccion[['year','pariciones']].\
            groupby("year").\
            sum().\
            reset_index().\
            sort_values(by=['pariciones'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    if query == 'hacienda':
        datos_produccion.ovejas = datos_produccion.ovejas.astype(int)
        mejor_año = datos_produccion[['year','ovejas']].\
            groupby("year").\
            max().\
            reset_index().\
            sort_values(by=['ovejas'], ascending=False, na_position='last').\
            head(1).\
            year.\
            values[0]

    return mejor_año

def df_is_valid(df, prod_colums, clima_columns):
    """
    Valida que el dataframe tenga todas las columnas 
    de produccion y de clima
    """
    return all(item in df.columns for item in prod_colums+clima_columns)


@login_required(login_url='login')
def mi_campo(request, query='rinde'):
    prod_columns = ['periodo','corderos','ovejas','carneros','pariciones','muertes','lana_producida','carne_producida','rinde_lana','finura_lana']
    clima_columns = ['periodo','temperatura_minima','temperatura_maxima','humedad','velocidad_viento','direccion_viento','mm_lluvia','localidad']
    campo = Campo.objects.get(persona=request.user.persona)
    df = campo.get_firebase_data()
    resultado = {}
    contexto = {}
    if campo and not df.empty and df_is_valid(df, prod_columns, clima_columns):
        df = df.fillna(0)
        datos_produccion = df[prod_columns]
        datos_climaticos = df[clima_columns]

        datos_climaticos['day'] = datos_climaticos.periodo.apply(lambda row:  row.day)
        datos_climaticos['month'] = datos_climaticos.periodo.apply(lambda row:  row.month)
        datos_climaticos['year'] = datos_climaticos.periodo.apply(lambda row:  row.year)

        datos_produccion['month'] = datos_produccion.periodo.apply(lambda row:  row.month)
        datos_produccion['day'] = datos_produccion.periodo.apply(lambda row:  row.day)
        datos_produccion['year'] = datos_produccion.periodo.apply(lambda row:  row.year)

        mejor_año = get_mejor_año_por_condicion(query, datos_produccion, datos_climaticos)

        datos = datos_climaticos[datos_climaticos.periodo.dt.year == mejor_año]
        datos_prod = datos_produccion[datos_produccion.periodo.dt.year == mejor_año]

        meses = sorted(list(set([d for d in datos.periodo.dt.month])))
        d_1 = datos
        d_2 = datos_prod
        for mes in meses: 
            d2 = d_1[d_1.month == mes]
            nombre_mes = get_nombre_mes(mes)
            resultado[nombre_mes] = {'dias': list(d2.day.to_list()),
                                     'temperatura_minima': min(d2.temperatura_minima.to_list()),
                                     'lluvia': list(d2.mm_lluvia.to_list()),
                                     'temperatura': d2.temperatura_minima.to_list(),
                                     'temperatura_maxima_list': d2.temperatura_maxima.to_list(),
                                     'temperatura_minima_list': d2.temperatura_minima.to_list(),
                                     'temperatura_maxima': max(d2.temperatura_maxima.to_list()),
                                     'viento_promedio': round(statistics.mean(list(d2.velocidad_viento.to_list()))),
                                     'humedad_promedio': round(statistics.mean(list(d2.humedad.to_list())))}
            d3 = d_2[d_2.month == mes]
            d3.ovejas = d3.ovejas.astype(int)
            d3.corderos = d3.corderos.astype(int)

            d3.rinde_lana = d3.rinde_lana.astype(int)
            d3.finura_lana = d3.finura_lana.astype(int)
            d3.carne_producida = d3.carne_producida.astype(int)
            d3.lana_producida = d3.lana_producida.astype(int)


            resultado[nombre_mes]['cant_ovejas'] = sum(list(d3.ovejas.to_list()))
            resultado[nombre_mes]['cant_corderos'] = sum(list(d3.corderos.to_list()))
            resultado[nombre_mes]['cant_carneros'] = sum(list(d3.corderos.to_list()))


            # En rinde se busca el Max, finura el Min, Carne y Lana Buscas la suma mensual
            resultado[nombre_mes]['rinde_lana_meses'] = max(list(d3.rinde_lana.to_list()))
            resultado[nombre_mes]['finura_lana_meses'] = min(list(d3.finura_lana.to_list()))
            resultado[nombre_mes]['cant_carne_meses'] = sum(list(d3.carne_producida.to_list()))
            resultado[nombre_mes]['cant_lana_meses'] = sum(list(d3.lana_producida.to_list()))

        contexto['resultado'] = resultado
        contexto['año'] = mejor_año
        contexto['query'] = query
        contexto['campo'] = campo
    else:
        messages.warning(request, "Debe cargar los datos climáticos de su campo.")
    return render(request, "mi_campo.html", contexto)


@login_required(login_url='login')
def datos_cargados(request):
    from datetime import datetime
    contexto={}
    contexto['campo_id'] = request.user.persona.campo.first().id
    contexto['fecha'] = str(datetime.now().date())
    columnas1 = [
    'corderos',
    'ovejas',
    'carneros',
    'pariciones']
    columnas2=[
    'muertes',
    'lana_producida',
    'carne_producida',
    'rinde_lana',
    'finura_lana']
    contexto['columnas1'] = columnas1
    contexto['columnas2'] = columnas2
    return render(request, "datos_cargados.html", contexto)
