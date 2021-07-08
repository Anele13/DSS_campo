from django.contrib import admin
from django.urls import path, include
from produccion.views import cargar_datos_produccion

urlpatterns = [
    path('carga_datos_produccion', cargar_datos_produccion, name="carga_datos_produccion"),
]