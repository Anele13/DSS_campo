from django.urls import path
from prediccion.views import prediccion_lana

urlpatterns = [
    path('prediccion_lana', prediccion_lana, name="prediccion_lana"),
]