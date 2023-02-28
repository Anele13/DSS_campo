from math import remainder
from django.db import models
from usuario.models import Persona
import requests
import firebase_admin
from firebase_admin import db
from datetime import datetime
from django.core.cache import cache
from sistema_campo.celery import app

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
        try:
            app_id = '439d4b804bc8187953eb36d2a8c26a02'
            url = f'https://openweathermap.org/data/2.5/weather?lat={self.latitud}&lon={self.longitud}&units=metric&appid={app_id}'
            cache_key = f'{self.latitud}{self.longitud}'
            cache_time = 86400 # time in seconds for cache to be valid
            data = cache.get(cache_key, {}) 
            if not data: 
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
                cache.set(cache_key, data, cache_time)
            return data 
        except Exception: #connection refused
            return {}

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


    def get_firebase_data(self):
        """
        Devuelve toda la informacion de un campo especifico
        """
        import pandas as pd
        campo_data = db.reference(f"campo/{self.id}/historico").get()
        resul = []
        if campo_data:
            for k, v in campo_data.items():
                v.update({'periodo': datetime.strptime(k, '%Y-%m-%d')})
                resul.append(v)
            if resul:
                return pd.DataFrame(resul)
        return pd.DataFrame() 


    def get_diaria_data(self):
        """
        Devuelve toda la informacion diaria de un campo
        """
        d = {}
        _diaria_data = db.reference(f"campo/{self.id}/diaria/").get()
        if _diaria_data:
            for k, v in _diaria_data.items():
                valor = 0
                try:
                    valor = int(v)
                except:
                    pass 
                d[k] = valor
        return d

    @app.task
    def registrar_info_climatica():
        now = datetime.now().date().strftime('%Y-%m-%d')
        for campo in Campo.objects.all():
            data = campo.clima_actual()
            if data:
                data.pop('temperatura') #Usado porque el campo temperatura no sirve, es la media
                _url = f"campo/{campo.id}/historico/{now}"
                _historico_data = db.reference(_url).get()
                if _historico_data:
                    _historico_data.update(data)
                    db.reference(_url).set(_historico_data)
                else: 
                    _info_produccion = {}
                    
                    _diaria_data = db.reference(f"campo/{campo.id}/diaria/").get()
                    if _diaria_data:
                        for k, v in _diaria_data.items():
                            valor = 0
                            try:
                                valor = int(v)
                            except:
                                pass 
                            _info_produccion[k] = valor
                    else:
                        _info_produccion['corderos'] = 0
                        _info_produccion['ovejas'] = 0
                        _info_produccion['carneros'] = 0
                   
                    _info_produccion['finura_lana'] = 0
                    _info_produccion['lana_producida'] = 0
                    _info_produccion['carne_producida'] = 0
                    _info_produccion['muertes'] = 0
                    _info_produccion['pariciones'] = 0
                    _info_produccion['rinde_lana'] = 0
                    _info_produccion.update(data)
                    db.reference(_url).set(_info_produccion)
                    



