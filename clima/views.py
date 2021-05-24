from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required(login_url='login')
def cargar_datos_climaticos(request):
    """
    Vista Inicio
    """
    return render(request, "alta_datos_climaticos.html")