from django.contrib import admin
from django.urls import path, include
from campo.views import mi_campo, datos_cargados

urlpatterns = [
    path('mi_campo', mi_campo, name="mi_campo"),
    path('mi_campo/<str:query>', mi_campo, name="mi_campo"),
    path('datos_cargados', datos_cargados, name="datos_cargados"),
]
