from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
    path('login', login_view, name="login"),
    path("logout",logout_view, name="logout"),
    path("registro",registro, name="registro"),
]
