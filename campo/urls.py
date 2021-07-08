from django.contrib import admin
from django.urls import path, include
from campo.views import mi_campo

urlpatterns = [
    path('mi_campo', mi_campo, name="mi_campo"),
]
