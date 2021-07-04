from django.contrib import admin
from django.urls import path, include
from .views import mostrar_filtros, buscador, mi_campo

urlpatterns = [
    path('mostrar_filtros', mostrar_filtros, name="mostrar_filtros"),
    path('buscador', buscador, name="buscador"),
    path('mi_campo', mi_campo, name="mi_campo"),
    
]
