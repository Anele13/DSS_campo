from django.db import models
import pandas as pd
from campo.models import Campo

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
        lista_columnas = ['periodo','temperatura_minima', 'temperatura_media',
                    'temperatura_maxima', 'humedad', 'velocidad_viento', 
                    'direccion_viento', 'velocidad_max_viento', 'barometro', 
                    'mm_lluvia', 'radiacion_solar']
        max_columnas = len(lista_columnas)
        print(df)

        """
        if (len(df.columns) != max_columnas):
            raise Exception("El archivo debe contener las siguientes columnas: " + ','.join(lista_columnas))
        
        if(not all(columna in lista_columnas for columna in df.columns.tolist())):
            raise Exception("El archivo ingresado tiene datos incorrectos.")

        df.insert(len(df.columns.tolist()), "sonda", self.id)
        conn = sqlite3.connect(BASE_DIR.as_posix()+'/db.sqlite3')
        df.to_sql("clima_datosclimaticos", conn, if_exists="append",index=False)
        conn.close()
        """
