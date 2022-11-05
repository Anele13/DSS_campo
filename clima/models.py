from django.db import models
from campo.models import Campo
from sistema_campo.settings import BASE_DIR
import requests

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
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE, related_name='datos_climaticos')


