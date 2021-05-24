from django.contrib import admin
from django.urls import path, include
from .views import cargar_datos_climaticos

urlpatterns = [
    path('carga_datos', cargar_datos_climaticos, name="carga_datos"),
]