from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json


@login_required(login_url='login')
def mostrar_filtros(request):
    contexto = {'valor': 0}
    return render(request, "mostrar_filtros.html", contexto)


'''@login_required(login_url='login')
def buscador(request):
    contexto = {}
    datos = {'anio': 2012,
             'enero': {'dia1': {'tmpmax': 38, 'tmpmin': 21}, 'dia2': {'tmpmax': 41, 'tmpmin': 18}},
             'febrero': {'dia1': {'tmpmax': 32, 'tmpmin': 17}, 'dia2': {'tmpmax': 31, 'tmpmin': 15}}}
    contexto['data'] = json.dumps(datos)

    return render(request, "resultados_filtros.html", contexto)'''


@login_required(login_url='login')
def buscador(request):
    contexto = {'anio': 2012,
                'enero': {'dia1': {'tmpmax': 38, 'tmpmin': 21}, 'dia2': {'tmpmax': 41, 'tmpmin': 18}},
                'febrero': {'dia1': {'tmpmax': 32, 'tmpmin': 17}, 'dia2': {'tmpmax': 31, 'tmpmin': 15}}}

    return render(request, "resultados_filtros.html", contexto)
