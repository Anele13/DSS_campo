from django.db import models
from usuario.models import Persona
from clima.models import Sonda

class Campo(models.Model):
    persona = models.ForeignKey(Persona, null=True, db_column='persona', on_delete=models.SET_NULL)
    sonda = models.ForeignKey(Sonda, null=True, db_column='sonda', on_delete=models.SET_NULL)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    cant_hectareas = models.IntegerField()
