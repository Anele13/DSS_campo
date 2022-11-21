from django.urls import path
from prediccion.views import predecir

urlpatterns = [
    path('predecir', predecir, name="predecir"),
    path('predecir/<str:query>', predecir, name="predecir"),
]