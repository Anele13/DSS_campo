from django.db import models

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
    inicio_actividad = models.DateField(blank=True, null=True)
    localidad = models.CharField(max_length=30, blank=True, null=True)
    id_inta = models.IntegerField(blank=True, null=True)


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
    sonda = models.ForeignKey(Sonda, null=True, db_column='sonda', on_delete=models.SET_NULL)

