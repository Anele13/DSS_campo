from lxml import html
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import os,re, sqlite3, request, OleFileIO_PL
from datetime import datetime
from calendar import monthrange


def get_sondas_inta():
    url_ppal = "http://sipas.inta.gob.ar/?q=agrometeorologia-listado-estaciones"
    url_info = 'http://sipas.inta.gob.ar/?q=agrometeorologia-detalle-estacion&idEstacion='

    #Obtener nombre y numero de estacion
    page = requests.get(url_ppal)
    response = html.fromstring(page.content)
    z = response.xpath('//div[@class="row"]/div/a/@href')
    c = response.xpath('//div[@class="row"]/div[@class="col-md-4 row-line"]')
    localidades = [ l.text.rstrip().lstrip() for l in c]

    localid = list(filter(None, localidades)) #saca las localidades vacias
    f = [str(d)[::-1].split('=')[0][::-1] for d in z]
    numeros = list(dict.fromkeys(f))
    resultado = dict(zip(localid,numeros))
    o = []
    for key, value in resultado.items():
        final={}
        page2 = requests.get(url_info+value)
        response2 = html.fromstring(page2.content)
        a = response2.xpath('//div[@class="divData"]/table[1]/tbody/tr')
        for x in a:
            if len(x) > 1:
                clave = str(x[0].text).replace(':','')
                valor = str(x[1].text).replace('-','')
            
                if '/' in clave: #lat, long y altura
                    final['latitud'] = str(x[1].text).split('/')[0].lstrip().rstrip()
                    final['longitud'] = str(x[1].text).split('/')[1].lstrip().rstrip()
                    final['altura'] = re.findall('\\d+',str(x[1].text).split('/')[2].lstrip().rstrip())
                else:
                    final[clave]=valor
                final['id_inta'] = value
        o.append(final)
    df = pd.DataFrame(o)
    #['nombre', 'latitud',  'longitud',  'altura',  'pertenencia',  'inicio_actividad', 'id_inta']
    df.to_csv('lista_informacion_estaciones.csv', index=False)

    #TODO: saco la id_inta = 20 porque no me anda bajar el excel con el otro script.
    #--------------------------------------------------------------------------------------


def get_info_climatica():
    anios = list(range(2005,2020)) #Dice 2021 pero te da del 2010 al 2020
    meses = list(range(1,13)) #Dice 13 pero te da una lista del 1 al 12
    lista_estaciones = ['11']

    df_total = pd.DataFrame()
    for estacion in lista_estaciones:
        for anio in anios:
            for mes in meses:
                url = F"http://sipas.inta.gob.ar/codesipas/web/app_dev.php/toExcel/{estacion}/{mes}/{anio}"
                resp = requests.get(url)
                ole = OleFileIO_PL.OleFileIO(resp.content)
                df = pd.read_excel(ole.openstream('Workbook'))
                df = df[1:] 
                df.columns = ['dia','temperatura_minima', 'temperatura_media', 'temperatura_maxima', 'humedad', 'velocidad_viento', 
                            'direccion_viento', 'velocidad_max_viento', 'barometro', 'mm_lluvia', 'radiacion_solar','eliminar']
                df = df[df.columns]
                df['sonda'] = estacion
                df.drop(df.tail(3).index,inplace = True)
                if len(df) > 31:
                    print(df)
                    fecha = datetime(year=anio, month=mes, day=1).date()
                    dia_corte = fecha.replace(day = monthrange(fecha.year, fecha.month)[1]).day
                    df = df.iloc[:dia_corte,:]
                print("-----------------")
                print(f'estacion:{estacion} anio:{anio} mes:{mes}')
                print("-----------------")  
                if (not df.empty):
                    df['periodo'] = df['dia'].apply(lambda dia: datetime.strptime(str(anio)+'-'+str(mes)+'-'+str(dia), '%Y-%m-%d'))
                df.drop(columns=['dia'], inplace=True)
                df_total = df_total.append(df)

    #TODO: ver si al excel hay que sacarle la primer fila que trae solo la fecha y no sirve.
    print(df_total)

if __name__ == '__main__':
    print("hola")
