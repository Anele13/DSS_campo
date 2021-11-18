from django.db import models
import pandas as pd
import sqlite3
from sistema_campo.settings import BASE_DIR
import json


class Sonda(models.Model):
    PERTENENCIA_CHOICES = (
        ("INTA", "INTA"),
        ("PARTICULAR", "PARTICULAR")
    )
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    ubicacion_exacta = models.CharField(max_length=200, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    pertenencia = models.CharField(max_length=15, choices=PERTENENCIA_CHOICES, default='1')
    inicio_actividad = models.CharField(max_length=30, blank=True, null=True)
    localidad = models.CharField(max_length=200, blank=True, null=True)
    id_inta = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def agregar_datos_climaticos(self, archivo):
        df = pd.read_csv(archivo)
        lista_columnas = ['periodo','temperatura_minima', 'temperatura_media',
                    'temperatura_maxima', 'humedad', 'velocidad_viento', 
                    'direccion_viento', 'velocidad_max_viento', 'barometro', 
                    'mm_lluvia', 'radiacion_solar']
        max_columnas = len(lista_columnas)

        if (len(df.columns) != max_columnas):
            raise Exception("El archivo debe contener las siguientes columnas: " + ','.join(lista_columnas))
        
        if(not all(columna in lista_columnas for columna in df.columns.tolist())):
            raise Exception("El archivo ingresado tiene datos incorrectos.")

        from sqlalchemy import create_engine
        DATABASE_URL ='postgresql://xgkvwrbclwgnyu:8b379f2bee4fdfefb3e6cfc4d80d302cbde023fdb5ef8043fa824e06bd3e9a85@ec2-34-204-128-77.compute-1.amazonaws.com:5432/debchq0b5cp3jb'
        df.insert(len(df.columns.tolist()), "sonda", self.id)
        #conn = sqlite3.connect(BASE_DIR.as_posix()+'/db.sqlite3')
        engine = create_engine(DATABASE_URL, echo = False)
        df.to_sql("clima_datosclimaticos", con=engine, if_exists="append",index=False)


    @classmethod
    def formatear(self, sondas):
        respuesta = {}  
        c = {"911000": {'nombre': 'prueba',
  'latitud': -43.29,
  'longitud': -68.71,
  'altura': 0},
 "911001": {'nombre': 'prueba',
  'latitud': -43.25,
  'longitud': -68.66,
  'altura': 0},
 "911002": {'nombre': 'prueba',
  'latitud': -43.22,
  'longitud': -68.62,
  'altura': 0},
 "911003": {'nombre': 'prueba',
  'latitud': -43.17,
  'longitud': -68.62,
  'altura': 0},
 "911004": {'nombre': 'prueba',
  'latitud': -43.12,
  'longitud': -68.64,
  'altura': 0},
 "911005": {'nombre': 'prueba',
  'latitud': -43.1,
  'longitud': -68.58,
  'altura': 0},
 "911006": {'nombre': 'prueba',
  'latitud': -43.07,
  'longitud': -68.55,
  'altura': 0},
 "911007": {'nombre': 'prueba',
  'latitud': -43.02,
  'longitud': -68.57,
  'altura': 0},
 "911008": {'nombre': 'prueba',
  'latitud': -42.97,
  'longitud': -68.58,
  'altura': 0},
 "911009": {'nombre': 'prueba',
  'latitud': -42.94,
  'longitud': -68.64,
  'altura': 0},
 "911010": {'nombre': 'prueba',
  'latitud': -42.89,
  'longitud': -68.68,
  'altura': 0},
 "911011": {'nombre': 'prueba',
  'latitud': -42.85,
  'longitud': -68.72,
  'altura': 0},
 "911012": {'nombre': 'prueba',
  'latitud': -42.81,
  'longitud': -68.77,
  'altura': 0},
 "911013": {'nombre': 'prueba',
  'latitud': -42.77,
  'longitud': -68.82,
  'altura': 0},
 "911014": {'nombre': 'prueba',
  'latitud': -42.75,
  'longitud': -68.88,
  'altura': 0},
 "911015": {'nombre': 'prueba',
  'latitud': -42.72,
  'longitud': -68.93,
  'altura': 0},
 "911016": {'nombre': 'prueba',
  'latitud': -42.7,
  'longitud': -69.0,
  'altura': 0},
 "911017": {'nombre': 'prueba',
  'latitud': -42.66,
  'longitud': -69.04,
  'altura': 0},
 "911018": {'nombre': 'prueba',
  'latitud': -42.62,
  'longitud': -69.08,
  'altura': 0},
 "911019": {'nombre': 'prueba',
  'latitud': -42.59,
  'longitud': -69.12,
  'altura': 0},
 "911020": {'nombre': 'prueba',
  'latitud': -42.58,
  'longitud': -69.16,
  'altura': 0},
 "911021": {'nombre': 'prueba',
  'latitud': -42.53,
  'longitud': -69.2,
  'altura': 0},
 "911022": {'nombre': 'prueba',
  'latitud': -42.48,
  'longitud': -69.2,
  'altura': 0},
 "911023": {'nombre': 'prueba',
  'latitud': -42.42,
  'longitud': -69.21,
  'altura': 0},
 "911024": {'nombre': 'prueba',
  'latitud': -42.37,
  'longitud': -69.22,
  'altura': 0},
 "911025": {'nombre': 'prueba',
  'latitud': -42.36,
  'longitud': -69.12,
  'altura': 0},
 "911026": {'nombre': 'prueba',
  'latitud': -42.39,
  'longitud': -69.03,
  'altura': 0},
 "911027": {'nombre': 'prueba',
  'latitud': -42.39,
  'longitud': -68.94,
  'altura': 0},
 "911028": {'nombre': 'prueba',
  'latitud': -42.39,
  'longitud': -68.85,
  'altura': 0},
 "911029": {'nombre': 'prueba',
  'latitud': -42.42,
  'longitud': -68.79,
  'altura': 0},
 "911030": {'nombre': 'prueba',
  'latitud': -42.47,
  'longitud': -68.71,
  'altura': 0},
 "911031": {'nombre': 'prueba',
  'latitud': -42.48,
  'longitud': -68.61,
  'altura': 0},
 "911032": {'nombre': 'prueba',
  'latitud': -42.83,
  'longitud': -68.38,
  'altura': 0},
 "911033": {'nombre': 'prueba',
  'latitud': -42.86,
  'longitud': -68.4,
  'altura': 0},
 "911034": {'nombre': 'prueba',
  'latitud': -42.92,
  'longitud': -68.42,
  'altura': 0},
 "911035": {'nombre': 'prueba',
  'latitud': -42.92,
  'longitud': -68.51,
  'altura': 0},
 "911036": {'nombre': 'prueba',
  'latitud': -42.96,
  'longitud': -68.58,
  'altura': 0},
 "911037": {'nombre': 'prueba',
  'latitud': -43.1,
  'longitud': -68.56,
  'altura': 0},
 "911038": {'nombre': 'prueba',
  'latitud': -43.14,
  'longitud': -68.52,
  'altura': 0},
 "911039": {'nombre': 'prueba',
  'latitud': -43.19,
  'longitud': -68.48,
  'altura': 0},
 "911040": {'nombre': 'prueba',
  'latitud': -43.25,
  'longitud': -68.43,
  'altura': 0},
 "911041": {'nombre': 'prueba',
  'latitud': -43.27,
  'longitud': -68.37,
  'altura': 0},
 "911042": {'nombre': 'prueba',
  'latitud': -43.25,
  'longitud': -68.28,
  'altura': 0},
 "911043": {'nombre': 'prueba',
  'latitud': -43.25,
  'longitud': -68.18,
  'altura': 0},
 "911044": {'nombre': 'prueba',
  'latitud': -43.27,
  'longitud': -68.12,
  'altura': 0},
 "911045": {'nombre': 'prueba',
  'latitud': -43.3,
  'longitud': -68.04,
  'altura': 0},
 "911046": {'nombre': 'prueba',
  'latitud': -43.31,
  'longitud': -67.97,
  'altura': 0},
 "911047": {'nombre': 'prueba',
  'latitud': -43.31,
  'longitud': -67.88,
  'altura': 0},
 "911048": {'nombre': 'prueba',
  'latitud': -43.31,
  'longitud': -67.82,
  'altura': 0},
 "911049": {'nombre': 'prueba',
  'latitud': -43.3,
  'longitud': -67.77,
  'altura': 0},
 "911050": {'nombre': 'prueba',
  'latitud': -43.79,
  'longitud': -67.32,
  'altura': 0},
 "911051": {'nombre': 'prueba',
  'latitud': -43.84,
  'longitud': -67.34,
  'altura': 0},
 "911052": {'nombre': 'prueba',
  'latitud': -43.88,
  'longitud': -67.34,
  'altura': 0},
 "911053": {'nombre': 'prueba',
  'latitud': -43.92,
  'longitud': -67.31,
  'altura': 0},
 "911054": {'nombre': 'prueba',
  'latitud': -43.96,
  'longitud': -67.29,
  'altura': 0},
 "911055": {'nombre': 'prueba',
  'latitud': -44.01,
  'longitud': -67.26,
  'altura': 0},
 "911056": {'nombre': 'prueba',
  'latitud': -44.06,
  'longitud': -67.25,
  'altura': 0},
 "911057": {'nombre': 'prueba',
  'latitud': -44.1,
  'longitud': -67.24,
  'altura': 0},
 "911058": {'nombre': 'prueba',
  'latitud': -44.14,
  'longitud': -67.2,
  'altura': 0},
 "911059": {'nombre': 'prueba',
  'latitud': -44.18,
  'longitud': -67.17,
  'altura': 0},
 "911060": {'nombre': 'prueba',
  'latitud': -44.22,
  'longitud': -67.17,
  'altura': 0},
 "911061": {'nombre': 'prueba',
  'latitud': -44.26,
  'longitud': -67.16,
  'altura': 0},
 "911062": {'nombre': 'prueba',
  'latitud': -44.29,
  'longitud': -67.13,
  'altura': 0},
 "911063": {'nombre': 'prueba',
  'latitud': -44.33,
  'longitud': -67.12,
  'altura': 0},
 "911064": {'nombre': 'prueba',
  'latitud': -44.36,
  'longitud': -67.08,
  'altura': 0},
 "911065": {'nombre': 'prueba',
  'latitud': -44.39,
  'longitud': -67.04,
  'altura': 0},
 "911066": {'nombre': 'prueba',
  'latitud': -44.4,
  'longitud': -66.99,
  'altura': 0},
 "911067": {'nombre': 'prueba',
  'latitud': -44.44,
  'longitud': -66.97,
  'altura': 0},
 "911068": {'nombre': 'prueba',
  'latitud': -44.47,
  'longitud': -66.96,
  'altura': 0},
 "911069": {'nombre': 'prueba',
  'latitud': -44.49,
  'longitud': -66.91,
  'altura': 0},
 "911070": {'nombre': 'prueba',
  'latitud': -44.57,
  'longitud': -66.98,
  'altura': 0},
 "911071": {'nombre': 'prueba',
  'latitud': -44.56,
  'longitud': -67.03,
  'altura': 0},
 "911072": {'nombre': 'prueba',
  'latitud': -44.55,
  'longitud': -67.06,
  'altura': 0},
 "911073": {'nombre': 'prueba',
  'latitud': -44.55,
  'longitud': -67.1,
  'altura': 0},
 "911074": {'nombre': 'prueba',
  'latitud': -44.54,
  'longitud': -67.16,
  'altura': 0},
 "911075": {'nombre': 'prueba',
  'latitud': -43.3,
  'longitud': -67.75,
  'altura': 0},
 "911076": {'nombre': 'prueba',
  'latitud': -43.35,
  'longitud': -67.72,
  'altura': 0},
 "911077": {'nombre': 'prueba',
  'latitud': -43.38,
  'longitud': -67.73,
  'altura': 0},
 "911078": {'nombre': 'prueba',
  'latitud': -43.42,
  'longitud': -67.69,
  'altura': 0},
 "911079": {'nombre': 'prueba',
  'latitud': -43.47,
  'longitud': -67.72,
  'altura': 0},
 "911080": {'nombre': 'prueba',
  'latitud': -43.48,
  'longitud': -67.65,
  'altura': 0},
 "911081": {'nombre': 'prueba',
  'latitud': -43.51,
  'longitud': -67.58,
  'altura': 0},
 "911082": {'nombre': 'prueba',
  'latitud': -43.52,
  'longitud': -67.51,
  'altura': 0},
 "911083": {'nombre': 'prueba',
  'latitud': -43.53,
  'longitud': -67.47,
  'altura': 0},
 "911084": {'nombre': 'prueba',
  'latitud': -43.55,
  'longitud': -66.72,
  'altura': 0},
 "911085": {'nombre': 'prueba',
  'latitud': -43.5,
  'longitud': -66.79,
  'altura': 0},
 "911086": {'nombre': 'prueba',
  'latitud': -43.46,
  'longitud': -66.86,
  'altura': 0},
 "911087": {'nombre': 'prueba',
  'latitud': -43.4,
  'longitud': -66.89,
  'altura': 0},
 "911088": {'nombre': 'prueba',
  'latitud': -43.34,
  'longitud': -66.97,
  'altura': 0},
 "911089": {'nombre': 'prueba',
  'latitud': -43.08,
  'longitud': -67.21,
  'altura': 0},
 "911090": {'nombre': 'prueba',
  'latitud': -43.02,
  'longitud': -67.25,
  'altura': 0},
 "911091": {'nombre': 'prueba',
  'latitud': -42.95,
  'longitud': -67.29,
  'altura': 0},
 "911092": {'nombre': 'prueba',
  'latitud': -42.92,
  'longitud': -67.37,
  'altura': 0},
 "911093": {'nombre': 'prueba',
  'latitud': -42.89,
  'longitud': -67.44,
  'altura': 0},
 "911094": {'nombre': 'prueba',
  'latitud': -42.88,
  'longitud': -67.52,
  'altura': 0},
 "911095": {'nombre': 'prueba',
  'latitud': -42.89,
  'longitud': -67.64,
  'altura': 0},
 "911096": {'nombre': 'prueba',
  'latitud': -43.34,
  'longitud': -67.22,
  'altura': 0},
 "911097": {'nombre': 'prueba',
  'latitud': -43.35,
  'longitud': -67.31,
  'altura': 0},
 "911098": {'nombre': 'prueba',
  'latitud': -43.37,
  'longitud': -67.39,
  'altura': 0},
 "911099": {'nombre': 'prueba',
  'latitud': -43.38,
  'longitud': -67.48,
  'altura': 0},
 "911100": {'nombre': 'prueba',
  'latitud': -43.5,
  'longitud': -67.78,
  'altura': 0},
 "911101": {'nombre': 'prueba',
  'latitud': -43.52,
  'longitud': -67.88,
  'altura': 0},
 "911102": {'nombre': 'prueba',
  'latitud': -43.54,
  'longitud': -67.96,
  'altura': 0},
 "911103": {'nombre': 'prueba',
  'latitud': -43.55,
  'longitud': -68.04,
  'altura': 0},
 "911104": {'nombre': 'prueba',
  'latitud': -43.54,
  'longitud': -68.15,
  'altura': 0},
 "911105": {'nombre': 'prueba',
  'latitud': -43.51,
  'longitud': -68.23,
  'altura': 0},
 "911106": {'nombre': 'prueba',
  'latitud': -43.51,
  'longitud': -68.32,
  'altura': 0},
 "911107": {'nombre': 'prueba',
  'latitud': -43.47,
  'longitud': -68.41,
  'altura': 0},
 "911108": {'nombre': 'prueba',
  'latitud': -43.44,
  'longitud': -68.51,
  'altura': 0},
 "911109": {'nombre': 'prueba',
  'latitud': -43.44,
  'longitud': -68.6,
  'altura': 0},
 "911110": {'nombre': 'prueba',
  'latitud': -43.46,
  'longitud': -68.81,
  'altura': 0},
 "911111": {'nombre': 'prueba',
  'latitud': -43.52,
  'longitud': -68.84,
  'altura': 0},
 "911112": {'nombre': 'prueba',
  'latitud': -43.56,
  'longitud': -68.9,
  'altura': 0},
 "911113": {'nombre': 'prueba',
  'latitud': -43.61,
  'longitud': -68.95,
  'altura': 0},
 "911114": {'nombre': 'prueba',
  'latitud': -43.7,
  'longitud': -68.93,
  'altura': 0},
 "911115": {'nombre': 'prueba',
  'latitud': -43.76,
  'longitud': -68.95,
  'altura': 0},
 "911116": {'nombre': 'prueba',
  'latitud': -44.0,
  'longitud': -69.15,
  'altura': 0},
 "911117": {'nombre': 'prueba',
  'latitud': -44.06,
  'longitud': -69.21,
  'altura': 0},
 "911118": {'nombre': 'prueba',
  'latitud': -44.11,
  'longitud': -69.27,
  'altura': 0},
 "911119": {'nombre': 'prueba',
  'latitud': -44.17,
  'longitud': -69.27,
  'altura': 0},
 "911120": {'nombre': 'prueba',
  'latitud': -44.23,
  'longitud': -69.33,
  'altura': 0},
 "911121": {'nombre': 'prueba',
  'latitud': -44.22,
  'longitud': -68.23,
  'altura': 0},
 "911122": {'nombre': 'prueba',
  'latitud': -44.29,
  'longitud': -68.29,
  'altura': 0},
 "911123": {'nombre': 'prueba',
  'latitud': -44.36,
  'longitud': -68.27,
  'altura': 0},
 "911124": {'nombre': 'prueba',
  'latitud': -44.42,
  'longitud': -68.25,
  'altura': 0},
 "911125": {'nombre': 'prueba',
  'latitud': -43.89,
  'longitud': -68.97,
  'altura': 0},
 "911126": {'nombre': 'prueba',
  'latitud': -43.91,
  'longitud': -68.89,
  'altura': 0},
 "911127": {'nombre': 'prueba',
  'latitud': -43.94,
  'longitud': -68.83,
  'altura': 0},
 "911128": {'nombre': 'prueba',
  'latitud': -43.95,
  'longitud': -68.77,
  'altura': 0},
 "911129": {'nombre': 'prueba',
  'latitud': -43.97,
  'longitud': -68.72,
  'altura': 0},
 "911130": {'nombre': 'prueba',
  'latitud': -44.0,
  'longitud': -68.66,
  'altura': 0},
 "911131": {'nombre': 'prueba',
  'latitud': -44.04,
  'longitud': -68.61,
  'altura': 0},
 "911132": {'nombre': 'prueba',
  'latitud': -44.08,
  'longitud': -68.54,
  'altura': 0},
 "911133": {'nombre': 'prueba',
  'latitud': -44.1,
  'longitud': -68.53,
  'altura': 0},
 "911134": {'nombre': 'prueba',
  'latitud': -44.13,
  'longitud': -68.49,
  'altura': 0},
 "911135": {'nombre': 'prueba',
  'latitud': -44.14,
  'longitud': -68.44,
  'altura': 0},
 "911136": {'nombre': 'prueba',
  'latitud': -44.14,
  'longitud': -68.38,
  'altura': 0},
 "911137": {'nombre': 'prueba',
  'latitud': -44.14,
  'longitud': -68.33,
  'altura': 0},
 "911138": {'nombre': 'prueba',
  'latitud': -44.16,
  'longitud': -68.27,
  'altura': 0},
 "911139": {'nombre': 'prueba',
  'latitud': -44.14,
  'longitud': -68.23,
  'altura': 0},
 "911140": {'nombre': 'prueba',
  'latitud': -44.12,
  'longitud': -68.16,
  'altura': 0},
 "911141": {'nombre': 'prueba',
  'latitud': -44.1,
  'longitud': -68.1,
  'altura': 0},
 "911142": {'nombre': 'prueba',
  'latitud': -44.11,
  'longitud': -68.03,
  'altura': 0},
 "911143": {'nombre': 'prueba',
  'latitud': -44.11,
  'longitud': -67.95,
  'altura': 0},
 "911144": {'nombre': 'prueba',
  'latitud': -44.07,
  'longitud': -67.92,
  'altura': 0},
 "911145": {'nombre': 'prueba',
  'latitud': -44.03,
  'longitud': -67.9,
  'altura': 0},
 "911146": {'nombre': 'prueba',
  'latitud': -44.0,
  'longitud': -67.85,
  'altura': 0},
 "911147": {'nombre': 'prueba',
  'latitud': -43.98,
  'longitud': -67.8,
  'altura': 0},
 "911148": {'nombre': 'prueba',
  'latitud': -43.99,
  'longitud': -67.74,
  'altura': 0},
 "911149": {'nombre': 'prueba',
  'latitud': -43.96,
  'longitud': -67.68,
  'altura': 0},
 "911150": {'nombre': 'prueba',
  'latitud': -42.78,
  'longitud': -65.99,
  'altura': 0},
 "911151": {'nombre': 'prueba',
  'latitud': -42.75,
  'longitud': -66.07,
  'altura': 0},
 "911152": {'nombre': 'prueba',
  'latitud': -42.7,
  'longitud': -66.18,
  'altura': 0},
 "911153": {'nombre': 'prueba',
  'latitud': -42.67,
  'longitud': -66.27,
  'altura': 0},
 "911154": {'nombre': 'prueba',
  'latitud': -42.63,
  'longitud': -66.36,
  'altura': 0},
 "911155": {'nombre': 'prueba',
  'latitud': -42.63,
  'longitud': -66.45,
  'altura': 0},
 "911156": {'nombre': 'prueba',
  'latitud': -42.59,
  'longitud': -66.52,
  'altura': 0},
 "911157": {'nombre': 'prueba',
  'latitud': -42.56,
  'longitud': -66.57,
  'altura': 0},
 "911158": {'nombre': 'prueba',
  'latitud': -42.53,
  'longitud': -66.65,
  'altura': 0},
 "911159": {'nombre': 'prueba',
  'latitud': -42.52,
  'longitud': -66.75,
  'altura': 0},
 "911160": {'nombre': 'prueba',
  'latitud': -42.48,
  'longitud': -66.83,
  'altura': 0},
 "911161": {'nombre': 'prueba',
  'latitud': -42.45,
  'longitud': -66.92,
  'altura': 0},
 "911162": {'nombre': 'prueba',
  'latitud': -42.45,
  'longitud': -67.02,
  'altura': 0},
 "911163": {'nombre': 'prueba',
  'latitud': -42.46,
  'longitud': -67.11,
  'altura': 0},
 "911164": {'nombre': 'prueba',
  'latitud': -42.44,
  'longitud': -67.2,
  'altura': 0},
 "911165": {'nombre': 'prueba',
  'latitud': -42.42,
  'longitud': -67.29,
  'altura': 0},
 "911166": {'nombre': 'prueba',
  'latitud': -42.38,
  'longitud': -67.37,
  'altura': 0},
 "911167": {'nombre': 'prueba',
  'latitud': -42.37,
  'longitud': -67.46,
  'altura': 0},
 "911168": {'nombre': 'prueba',
  'latitud': -42.37,
  'longitud': -67.56,
  'altura': 0},
 "911169": {'nombre': 'prueba',
  'latitud': -42.37,
  'longitud': -67.66,
  'altura': 0},
 "911170": {'nombre': 'prueba',
  'latitud': -42.4,
  'longitud': -67.74,
  'altura': 0},
 "911171": {'nombre': 'prueba',
  'latitud': -42.45,
  'longitud': -67.82,
  'altura': 0},
 "911172": {'nombre': 'prueba',
  'latitud': -42.49,
  'longitud': -67.9,
  'altura': 0},
 "911173": {'nombre': 'prueba',
  'latitud': -42.52,
  'longitud': -67.99,
  'altura': 0},
 "911174": {'nombre': 'prueba',
  'latitud': -42.53,
  'longitud': -68.09,
  'altura': 0},
 "911175": {'nombre': 'prueba',
  'latitud': -42.85,
  'longitud': -67.96,
  'altura': 0},
 "911176": {'nombre': 'prueba',
  'latitud': -42.81,
  'longitud': -68.02,
  'altura': 0},
 "911177": {'nombre': 'prueba',
  'latitud': -42.75,
  'longitud': -68.05,
  'altura': 0},
 "911178": {'nombre': 'prueba',
  'latitud': -42.69,
  'longitud': -68.07,
  'altura': 0},
 "911179": {'nombre': 'prueba',
  'latitud': -42.63,
  'longitud': -68.07,
  'altura': 0},
 "911180": {'nombre': 'prueba',
  'latitud': -42.57,
  'longitud': -68.13,
  'altura': 0},
 "911181": {'nombre': 'prueba',
  'latitud': -42.53,
  'longitud': -68.21,
  'altura': 0},
 "911182": {'nombre': 'prueba',
  'latitud': -42.55,
  'longitud': -68.27,
  'altura': 0},
 "911183": {'nombre': 'prueba',
  'latitud': -42.62,
  'longitud': -68.27,
  'altura': 0},
 "911184": {'nombre': 'prueba',
  'latitud': -42.67,
  'longitud': -68.23,
  'altura': 0},
 "911185": {'nombre': 'prueba',
  'latitud': -42.72,
  'longitud': -68.26,
  'altura': 0},
 "911186": {'nombre': 'prueba',
  'latitud': -42.77,
  'longitud': -68.22,
  'altura': 0},
 "911187": {'nombre': 'prueba',
  'latitud': -42.81,
  'longitud': -68.18,
  'altura': 0},
 "911188": {'nombre': 'prueba',
  'latitud': -42.83,
  'longitud': -68.1,
  'altura': 0},
 "911189": {'nombre': 'prueba',
  'latitud': -42.88,
  'longitud': -68.05,
  'altura': 0},
 "911190": {'nombre': 'prueba',
  'latitud': -42.87,
  'longitud': -67.98,
  'altura': 0},
 "911191": {'nombre': 'prueba',
  'latitud': -42.53,
  'longitud': -66.75,
  'altura': 0},
 "911192": {'nombre': 'prueba',
  'latitud': -42.53,
  'longitud': -66.81,
  'altura': 0},
 "911193": {'nombre': 'prueba',
  'latitud': -42.56,
  'longitud': -66.84,
  'altura': 0},
 "911194": {'nombre': 'prueba',
  'latitud': -42.6,
  'longitud': -66.85,
  'altura': 0},
 "911195": {'nombre': 'prueba',
  'latitud': -42.6,
  'longitud': -65.94,
  'altura': 0},
 "911196": {'nombre': 'prueba',
  'latitud': -42.58,
  'longitud': -65.99,
  'altura': 0},
 "911197": {'nombre': 'prueba',
  'latitud': -42.54,
  'longitud': -66.03,
  'altura': 0},
 "911198": {'nombre': 'prueba',
  'latitud': -42.52,
  'longitud': -66.08,
  'altura': 0},
 "911199": {'nombre': 'prueba',
  'latitud': -42.5,
  'longitud': -66.13,
  'altura': 0}}
        #TODO sacar esto que esta horrible 
        for s in sondas:
            if s.latitud and s.longitud:
                respuesta[str(s.id)] = {'nombre': s.nombre,
                                        'latitud': s.latitud,
                                        'longitud': s.longitud,
                                        'altura': 0}
        
        respuesta.update(c)
        return json.dumps(respuesta)



class DatosClimaticos(models.Model):
    periodo = models.DateField(blank=True, null=True)
    temperatura_minima = models.FloatField(blank=True, null=True)
    temperatura_media = models.FloatField(blank=True, null=True)
    temperatura_maxima = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    velocidad_viento = models.FloatField(blank=True, null=True)
    direccion_viento = models.CharField(max_length=100, blank=True, null=True)
    velocidad_max_viento = models.FloatField(blank=True, null=True)
    barometro = models.FloatField(blank=True, null=True)
    mm_lluvia = models.FloatField(blank=True, null=True)
    radiacion_solar = models.FloatField(blank=True, null=True)
    sonda = models.ForeignKey(Sonda, null=True, db_column='sonda', on_delete=models.SET_NULL, related_name='datos_climaticos_set')

