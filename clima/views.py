from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json

@login_required(login_url='login')
def cargar_datos_climaticos(request):
    contexto={}
    #Deben ser mas sondas pero luego sacamos mas..
    sondas = {'2':{'nombre':'28 de Julio','latitud':-43.24,'longitud': -65.48,'altura': 36},
              '15':{'nombre':'Arroyo Pescado','latitud':-42.58,'longitud': -70.38,'altura': 545}}
    contexto['sondas'] = json.dumps(sondas)
    if request.method == 'POST':
            messages.success(request, 'Alta de datos correcta!')
    return render(request, "alta_datos_climaticos.html",contexto)


@login_required(login_url='login')
def cargar_datos_produccion(request):
    contexto={}
    if request.method == 'POST':
        messages.success(request, 'Alta de datos correcta!')
    return render(request, "alta_datos_produccion.html",contexto)