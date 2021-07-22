from django.db import models
import pandas as pd
from campo.models import Campo
import sqlite3
from sistema_campo.settings import BASE_DIR

class DatosProduccion(models.Model):
    periodo =  models.DateField(blank=True, null=True)
    cantidad_corderos = models.IntegerField(blank=True, null=True)
    cantidad_ovejas = models.IntegerField(blank=True, null=True)
    cantidad_carneros = models.IntegerField(blank=True, null=True)
    cantidad_pariciones = models.IntegerField(blank=True, null=True)
    cantidad_muertes_corderos = models.IntegerField(blank=True, null=True)
    cantidad_lana_producida = models.IntegerField(blank=True, null=True)
    cantidad_carne_producida = models.IntegerField(blank=True, null=True)
    rinde_lana = models.IntegerField(blank=True, null=True)
    finura_lana = models.IntegerField(blank=True, null=True)
    campo = models.ForeignKey(Campo, null=True, db_column='campo', on_delete=models.SET_NULL, related_name='datos_produccion_set')


    @classmethod
    def agregar_datos_produccion(self, archivo, campo):
        df = pd.read_csv(archivo)
        lista_columnas = ['periodo', 'cantidad_corderos', 'cantidad_ovejas', 'cantidad_carneros',
                            'cantidad_pariciones', 'cantidad_muertes_corderos',
                            'cantidad_lana_producida', 'cantidad_carne_producida', 'rinde_lana',
                            'finura_lana']
        max_columnas = len(lista_columnas)
        if (len(df.columns) != max_columnas):
            raise Exception("El archivo debe contener las siguientes columnas: " + ','.join(lista_columnas))
        
        if(not all(columna in lista_columnas for columna in df.columns.tolist())):
            raise Exception("El archivo ingresado tiene datos incorrectos.")

        df.insert(len(df.columns.tolist()), "campo", campo.id)
        conn = sqlite3.connect(BASE_DIR.as_posix()+'/db.sqlite3')
        df.to_sql("produccion_datosproduccion", conn, if_exists="append",index=False)
        conn.close()