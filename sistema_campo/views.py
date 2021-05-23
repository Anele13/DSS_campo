from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


@login_required(login_url='login')
def inicio(request):
    """
    Vista Inicio
    """
    return render(request, "bienvenido.html")