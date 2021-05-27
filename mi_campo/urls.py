from django.contrib import admin
from django.urls import path, include
from .views import mostrar_filtros, buscador

urlpatterns = [
    path('mostrar_filtros', mostrar_filtros, name="mostrar_filtros"),
    path('buscador', buscador, name="buscador"),
]
