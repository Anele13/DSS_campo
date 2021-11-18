from lxml import html
from collections import Counter
import pandas as pd
import re,requests, OleFileIO_PL, io
from datetime import datetime
from calendar import monthrange
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        df = pd.read_csv('/home/anele/Escritorio/lista_informacion_estaciones.csv')
        #df = get_info_climatica()
        df = df[['id_inta','Inicio actividad']]
        r = dict(sorted(df.values.tolist()))
        df_total = pd.DataFrame()  
        for id_sonda, año_inicio in r.items():
            año_inicio = int(re.findall(r'\d+',año_inicio)[0]) #subcero porque devuelve una lista
            df = get_info_climatica(str(id_sonda), año_inicio)
            df_total = df_total.append(df)
        df_total.to_csv('/home/anele/Escritorio/info_climatica_todas_las_sondas_100.csv', index=False)
        """


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
    df.to_csv('/home/anele/Escritorio/lista_informacion_estaciones.csv', index=False)
    return df

def get_info_climatica(id_sonda, año_inicio):
    """
    anios = list(range(2005,2020)) 
    meses = list(range(1,13)) 
    lista_estaciones = ['3', '15', '50', '60', '62', '25', '54', '8', '5', '6', '63', 
                        '47', '46', '45', '7', '44', '41', '39', '61', '53', '57', '48', 
                        '2', '55', '71', '56', '16', '43', '51', '9', '58', '68', '17', '40',
                        '64', '11', '12', '4', '42', '10', '13', '49', '34', '19', '52', '20',
                        '65', '66', '73', '21', '70', '22', '1', '72', '23', '67', '24', '9']
    """
    meses = list(range(1,13)) 
    lista_estaciones = [id_sonda]
    anios = list(range(año_inicio,2021)) 
    df_total = pd.DataFrame()
    for estacion in lista_estaciones:
        for anio in anios:
            for mes in meses:
                url = F"http://sipas.inta.gob.ar/codesipas/web/app_dev.php/toExcel/{estacion}/{mes}/{anio}"
                toread = io.BytesIO()
                toread.write(requests.get(url).content)
                ole = OleFileIO_PL.OleFileIO(toread)
                df = pd.read_excel(ole.openstream('Workbook'))
                df = df[1:] 
                df.columns = ['dia','temperatura_media', 'temperatura_maxima', 'temperatura_minima', 'humedad', 'velocidad_viento', 
                            'direccion_viento', 'velocidad_max_viento', 'barometro', 'mm_lluvia', 'radiacion_solar','eliminar']
                df = df[df.columns]
                df['sonda'] = estacion
                df.drop(df.tail(3).index,inplace = True)
                if len(df) > 31:
                    fecha = datetime(year=anio, month=mes, day=1).date()
                    dia_corte = fecha.replace(day = monthrange(fecha.year, fecha.month)[1]).day
                    df = df.iloc[:dia_corte,:]
                print("-----------------")
                print(f'estacion:{estacion} anio:{anio} mes:{mes}')
                if (not df.empty):
                    df['periodo'] = df['dia'].apply(lambda dia: datetime.strptime(str(anio)+'-'+str(mes)+'-'+str(dia), '%Y-%m-%d'))
                df.drop(columns=['dia'], inplace=True)
                df_total = df_total.append(df)
    return df_total


def sondas_a_base():
    df = pd.read_csv('/home/anele/Escritorio/lista_informacion_estaciones.csv')
    df.rename(columns={'Identificación':'nombre',
                        'Inicio actividad':'inicio_actividad',
                        'Ubicación exacta':'ubicacion_exacta',
                        'Localidad':'localidad',
                        'latitud':'latitud',
                        'longitud':'longitud',
                        'Pertenencia':'pertenencia'}, inplace=True)
    df = df[['nombre',
            'latitud',
            'longitud',
            'altura',
            'pertenencia',
            'inicio_actividad',
            'localidad',
            'id_inta',
            'ubicacion_exacta']]
    
    df.dropna(inplace=True)
    df['id'] = df['id_inta']
    df.pertenencia = 'INTA'
    df = df.set_index('id').reset_index()
    df.latitud = df.latitud.apply(lambda row: -1* float('.'.join(re.findall(r'\d+', row)[:2])))
    df.longitud = df.longitud.apply(lambda row: -1* float('.'.join(re.findall(r'\d+', row)[:2])))
    df.altura = 0
    
    df.to_csv('nuevas_sondas.csv', header=False)
    

def clima_a_base():
    #falta leer DF
    df = df[['periodo','temperatura_minima', 'temperatura_media', 'temperatura_maxima',
            'humedad', 'velocidad_viento','velocidad_max_viento','barometro', 'mm_lluvia', 
            'radiacion_solar', 'sonda', 'direccion_viento']]


