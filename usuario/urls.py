from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    path('login', login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("registro", registro, name="registro"),
    path('perfil', perfil_view, name="perfil"),
    path('edicion', editar_perfil_view, name="edicion"),
    path('telegram_users', telegram_users, name="telegram_users"),
    path('desvincular_usuario', desvincular_user_telegram, name="desvincular_usuario"),
    ]
