from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def predecir_por_filtro(filtro):
    label_estimacion = None
    label_datos = None
    flag_filtro = None
    if filtro == 'lana':
        print('Lanaa')
        flag_filtro = 'Kg de lana'
    elif filtro== 'corderos':
        print('Corderos')
        flag_filtro = 'Cantidad de corderos'
    return label_estimacion, label_datos, flag_filtro

@login_required(login_url='login')
def predecir(request,query='lana'):
    label_datos, label_estimacion, flag_filtro = predecir_por_filtro(query)
    contexto = {}
    contexto["label_datos"] = label_datos
    contexto["label_estimacion"] = label_estimacion
    contexto["flag_filtro"] = flag_filtro
    return render(request, "prediccion.html", contexto)
