from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json
from .models import Campo


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


'''@login_required(login_url='login')
def buscador(request):
    contexto = {'anio': 2012,
                'enero': {'dia1': {'tmpmax': 38, 'tmpmin': 21}, 'dia2': {'tmpmax': 41, 'tmpmin': 18}},
                'febrero': {'dia1': {'tmpmax': 32, 'tmpmin': 17}, 'dia2': {'tmpmax': 31, 'tmpmin': 15}}}

    return render(request, "resultados_filtros.html", contexto)'''


@login_required(login_url='login')
def mi_campo(request):
    campo = Campo.objects.get(persona=request.user.persona)
    datos_climaticos = campo.sonda.datos_climaticos_set.all()
    print(datos_climaticos)

    contexto = {
        'anio': 2012,
        'meses': {
            'enero': {
                'promtemmax': 35,
                'promtemmin': 18,
                'dia1': {'tmpmax': 38, 'tmpmin': 21, 'precipitacion': 22},
                'dia2': {'tmpmax': 36, 'tmpmin': 17, 'precipitacion': 0},
                'dia3': {'tmpmax': 37, 'tmpmin': 18, 'precipitacion': 0},
                'dia4': {'tmpmax': 35, 'tmpmin': 20, 'precipitacion': 0},
                'dia5': {'tmpmax': 40, 'tmpmin': 22, 'precipitacion': 0},
                'dia6': {'tmpmax': 32, 'tmpmin': 16, 'precipitacion': 0},
                'dia7': {'tmpmax': 33, 'tmpmin': 16, 'precipitacion': 2},
                'dia8': {'tmpmax': 28, 'tmpmin': 14, 'precipitacion': 15},
                'dia9': {'tmpmax': 28, 'tmpmin': 14, 'precipitacion': 30},
                'dia10': {'tmpmax': 27, 'tmpmin': 15, 'precipitacion': 0}
            },
            'febrero': {
                'promtemmax': 31,
                'promtemmin': 15,
                'dia1': {'tmpmax': 31, 'tmpmin': 15, 'precipitacion': 5},
                'dia2': {'tmpmax': 32, 'tmpmin': 17, 'precipitacion': 0},
                'dia3': {'tmpmax': 33, 'tmpmin': 18, 'precipitacion': 0},
                'dia4': {'tmpmax': 35, 'tmpmin': 16, 'precipitacion': 0},
                'dia5': {'tmpmax': 28, 'tmpmin': 15, 'precipitacion': 10},
                'dia6': {'tmpmax': 29, 'tmpmin': 16, 'precipitacion': 0},
                'dia7': {'tmpmax': 25, 'tmpmin': 16, 'precipitacion': 2},
                'dia8': {'tmpmax': 26, 'tmpmin': 14, 'precipitacion': 15},
                'dia9': {'tmpmax': 28, 'tmpmin': 14, 'precipitacion': 30},
                'dia10': {'tmpmax': 27, 'tmpmin': 15, 'precipitacion': 0}
            },
            'marzo': {
                'promtemmax': 28,
                'promtemmin': 14,
                'dia1': {'tmpmax': 28, 'tmpmin': 15, 'precipitacion': 0},
                'dia2': {'tmpmax': 32, 'tmpmin': 16, 'precipitacion': 0},
                'dia3': {'tmpmax': 33, 'tmpmin': 18, 'precipitacion': 0},
                'dia4': {'tmpmax': 29, 'tmpmin': 15, 'precipitacion': 0},
                'dia5': {'tmpmax': 28, 'tmpmin': 15, 'precipitacion': 0},
                'dia6': {'tmpmax': 26, 'tmpmin': 14, 'precipitacion': 0},
                'dia7': {'tmpmax': 25, 'tmpmin': 16, 'precipitacion': 0},
                'dia8': {'tmpmax': 26, 'tmpmin': 13, 'precipitacion': 15},
                'dia9': {'tmpmax': 24, 'tmpmin': 14, 'precipitacion': 30},
                'dia10': {'tmpmax': 27, 'tmpmin': 15, 'precipitacion': 0}
            },
            'abril': {
                'promtemmax': 25,
                'promtemmin': 12,
                'dia1': {'tmpmax': 26, 'tmpmin': 13, 'precipitacion': 0},
                'dia2': {'tmpmax': 25, 'tmpmin': 14, 'precipitacion': 0},
                'dia3': {'tmpmax': 23, 'tmpmin': 11, 'precipitacion': 0},
                'dia4': {'tmpmax': 24, 'tmpmin': 12, 'precipitacion': 0},
                'dia5': {'tmpmax': 26, 'tmpmin': 15, 'precipitacion': 0},
                'dia6': {'tmpmax': 26, 'tmpmin': 14, 'precipitacion': 0},
                'dia7': {'tmpmax': 22, 'tmpmin': 10, 'precipitacion': 0},
                'dia8': {'tmpmax': 23, 'tmpmin': 13, 'precipitacion': 0},
                'dia9': {'tmpmax': 24, 'tmpmin': 14, 'precipitacion': 0},
                'dia10': {'tmpmax': 27, 'tmpmin': 15, 'precipitacion': 0}
            },
        }
    }

    contexto['resultados'] = json.dumps(contexto)

    return render(request, "resultados_filtros_v4.html", contexto)