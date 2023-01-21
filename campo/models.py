from math import remainder
from django.db import models
from usuario.models import Persona
import requests
import firebase_admin
from firebase_admin import db
from datetime import datetime


DATABASE_URL = 'https://dss-campo-default-rtdb.firebaseio.com/'
CREDENTIALS = 'dss-campo-firebase-adminsdk-3mpy4-19ac4df912.json'

firebase_admin.initialize_app(firebase_admin.credentials.Certificate(CREDENTIALS), {'databaseURL':DATABASE_URL})

class Campo(models.Model):
    persona = models.ForeignKey(Persona, null=True, on_delete=models.SET_NULL, related_name='campo')
    nombre = models.CharField(max_length=30, blank=True, null=True)
    cant_hectareas = models.IntegerField()
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    def clima_actual(self):
        """
        Retorna el clima actual del campo en el
        momento de la solicitud
        """
        data = {}
        if self.latitud and self.longitud:
            app_id = '439d4b804bc8187953eb36d2a8c26a02'
            url = f'https://openweathermap.org/data/2.5/weather?lat={self.latitud}&lon={self.longitud}&units=metric&appid={app_id}'
            response = requests.get(url).json()
            base_info = response.get('main',{})
            rain_info = response.get('rain',{})
            wind_info = response.get('wind',{})
            data['temperatura_minima'] = base_info.get('temp_min',0)
            data['temperatura_maxima'] = base_info.get('temp_max',0)
            data['temperatura'] = base_info.get('temp',0)
            data['humedad'] = base_info.get('humidity',0)
            data['velocidad_viento'] = wind_info.get('speed',0)
            data['direccion_viento'] = wind_info.get('deg',0)
            data['mm_lluvia'] = rain_info.get('1h',0)
            data['localidad'] = response.get('name',None)
        return data 

    def ultimo_registro_produccion(self):
        """
        Retorna el ultimo registro del campo al
        momento de la solicitud
        """
        data={}
        response = db.reference(f'campo/{self.id}').\
                    order_by_key().\
                    limit_to_last(1).\
                    get()
        if response:
            data['nacimientos'] = response.get('nacimientos',0)
            data['muertes'] = response.get('muertes',0)
            data['ventas'] = response.get('ventas',0)
            data['compras'] = response.get('compras',0)
        return data

    def historico_datos_climaticoss(self):
        """
        Obtiene desde firebase el historico de 
        datos climaticos registrados
        """
        data = {}
        return data

    def historico_datos_produccion(self):
        """
        Obtiene desde firebase el historico de 
        datos de produccion registrados
        """
        data = {}
        return data

    def create_in_firebase(self):
        from django.conf import settings
        data = settings.DIARIA
        db.reference(f'campo/{self.id}/diaria/').set(data)