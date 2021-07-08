from django.db import models
from usuario.models import Persona
from campo.models import Campo


class DatosProduccion(models.Model):
    periodo = models.DateField(blank=True, null=True)
    cantidad_corderos = models.IntegerField(blank=True, null=True)
    cantidad_ovejas = models.IntegerField(blank=True, null=True)
    cantidad_carneros = models.IntegerField(blank=True, null=True)
    cantidad_pariciones = models.IntegerField(blank=True, null=True)
    cantidad_muertes_corderos = models.IntegerField(blank=True, null=True)
    cantidad_lana_producida = models.IntegerField(blank=True, null=True)
    cantidad_carne_producida = models.IntegerField(blank=True, null=True)
    rinde_lana = models.IntegerField(blank=True, null=True)
    finura_lana = models.IntegerField(blank=True, null=True)
    campo = models.ForeignKey(Campo, null=True, db_column='campo',
                              on_delete=models.SET_NULL, related_name='datos_produccion_set')
