from django.db import models
import pandas as pd
import sqlite3
from sistema_campo.settings import BASE_DIR


class Sonda(models.Model):
    PERTENENCIA_CHOICES = (
        ("INTA", "INTA"),
        ("PARTICULAR", "PARTICULAR")
    )
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    ubicacion_exacta = models.CharField(max_length=30, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    altura = models.FloatField(blank=True, null=True)
    pertenencia = models.CharField(max_length=15, choices=PERTENENCIA_CHOICES, default='1')
    inicio_actividad = models.CharField(max_length=30, blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
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

        df.insert(len(df.columns.tolist()), "sonda", self.id)
        conn = sqlite3.connect(BASE_DIR.as_posix()+'/db.sqlite3')
        df.to_sql("clima_datosclimaticos", conn, if_exists="append",index=False)
        conn.close()


class DatosClimaticos(models.Model):
    periodo = models.DateField(blank=True, null=True)
    temperatura_minima = models.FloatField(blank=True, null=True)
    temperatura_media = models.FloatField(blank=True, null=True)
    temperatura_maxima = models.FloatField(blank=True, null=True)
    humedad = models.FloatField(blank=True, null=True)
    velocidad_viento = models.FloatField(blank=True, null=True)
    direccion_viento = models.FloatField(blank=True, null=True)
    velocidad_max_viento = models.FloatField(blank=True, null=True)
    barometro = models.FloatField(blank=True, null=True)
    mm_lluvia = models.FloatField(blank=True, null=True)
    radiacion_solar = models.FloatField(blank=True, null=True)
    sonda = models.ForeignKey(Sonda, null=True, db_column='sonda', on_delete=models.SET_NULL, related_name='datos_climaticos_set')

