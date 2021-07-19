from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    path('login', login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("registro", registro, name="registro"),
    path('miperfil', perfil_view, name="miperfil"),
    path('editarperfil/<pk>', editar_perfil_view, name="editarperfil"),
    #url(r'editarperfil/(?P<pk>[-\w]+)$',editar_perfil_view, name='editarperfil'),
]
