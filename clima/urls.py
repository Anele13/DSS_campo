from django.contrib import admin
from django.urls import path, include
from clima.views import cargar_datos_climaticos
urlpatterns = [
    path('carga_datos_climaticos', cargar_datos_climaticos, name="carga_datos_climaticos"),
]
