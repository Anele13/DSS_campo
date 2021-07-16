from django.db import models
from django.contrib.auth.models import User


class Persona(models.Model):
    documento = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='persona')
