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

        
        from sqlalchemy import create_engine
        DATABASE_URL ='postgresql://xgkvwrbclwgnyu:8b379f2bee4fdfefb3e6cfc4d80d302cbde023fdb5ef8043fa824e06bd3e9a85@ec2-34-204-128-77.compute-1.amazonaws.com:5432/debchq0b5cp3jb'
        df.insert(len(df.columns.tolist()), "campo", campo.id)
        #conn = sqlite3.connect(BASE_DIR.as_posix()+'/db.sqlite3')
        engine = create_engine(DATABASE_URL, echo = False)
        df.to_sql("produccion_datosproduccion", con=engine, if_exists="append",index=False)

        