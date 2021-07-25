from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import pandas as pd
from statsmodels.iolib.smpickle import load_pickle

from .models import DatosClimaticos, Sonda
from campo.models import Campo
from usuario.models import Persona
from usuario.views import get_persona_campo
import json
from sistema_campo.settings import BASE_DIR
from datetime import datetime
from django.contrib.staticfiles.storage import staticfiles_storage


@login_required(login_url='login')
def cargar_datos_climaticos(request):
    contexto = {}
    user = request.user
    if request.method == 'POST':
        try:
            campo = Campo.objects.get(persona=user.persona)
            if 'archivo_csv' in request.FILES:
                archivo_climatico = request.FILES['archivo_csv']
                campo.get_or_create_sonda().agregar_datos_climaticos(archivo_climatico)
                messages.success(request, "Datos registrados exitosamente")
            else:
                latitud = request.POST.get('latitud')
                longitud = request.POST.get('longitud')
                sonda = Sonda.objects.get(latitud=latitud, longitud=longitud)
                campo.sonda = sonda
                campo.save()
                sondas = Sonda.objects.filter(pertenencia='INTA')
                contexto['sondas'] = Sonda.formatear(sondas)
                messages.success(request, "Sonda cargada exitosamente")
        except Exception as e:
            messages.warning(request,str(e))
    else:
        persona, campo = get_persona_campo(user)
        if not (persona and campo):
            messages.warning(request, "Cargue sus datos personales y de su campo.")
        else:
            sondas = Sonda.objects.filter(pertenencia='INTA')
            contexto['sondas'] = Sonda.formatear(sondas)
    return render(request, "alta_datos_climaticos.html", contexto)


def format(dicc):
    """
    Devuelve un diccionario en forma de coordenadas x, y
    a partir de un dataframe con 2 columnas
    """
    resultado=[]
    for k, v in dicc.items():
        resul={}
        resul["x"]= k.strftime('%Y-%m-%d')
        resul["y"]=v
        resultado.append(resul)
    return resultado

def estimar(datos_climaticos, variable_estimacion):
    label_estimacion = None
    label_datos = None
    funcion_agrupamiento = None
    flag_filtro = None

    if variable_estimacion == 'mm_lluvia':
        path = staticfiles_storage.path('data/modelo_lluvia.pickle')
        label_datos = 'Lluvia Observada'
        label_estimacion = 'Estimacion de Lluvia'
        flag_filtro = "Mm de Lluvia Anuales"

    elif variable_estimacion == 'temperatura_maxima':
        path = staticfiles_storage.path('data/modelo_temperatura.pickle')
        label_datos = 'Temperatura Observada'
        label_estimacion = 'Estimacion de Temperatura'
        flag_filtro = "Temperaturas Maximas Anuales"
    else:
        raise Exception("La variable ingresada no corresponde en el modelo.")

    df= pd.DataFrame(datos_climaticos.values('periodo', variable_estimacion))
    df[['periodo']] = pd.to_datetime(df['periodo'])
    df.set_index('periodo',inplace=True)
    df.index.name = None
    if variable_estimacion == 'mm_lluvia':
        df= df[variable_estimacion].resample('MS').mean()
    else:
        df= df[variable_estimacion].resample('MS').max()

    df= df.fillna(df.bfill())

    #cargo el modelo entrenado
    
    results = load_pickle(path)

    #datos originales
    datos_sonda = format(df.to_dict())

    #estimacion climatica
    pred_uc = results.get_forecast(steps=10)
    datos_prediccion = format(pred_uc.predicted_mean.to_dict())

    #intervalos de confianza
    pred_ci = pred_uc.conf_int()
    intervalo_bajo = format(pred_ci[['lower '+variable_estimacion]].to_dict()['lower '+variable_estimacion])
    intervalo_alto =format(pred_ci[['upper '+variable_estimacion]].to_dict()['upper '+variable_estimacion])
    
    return datos_sonda, datos_prediccion, intervalo_bajo, intervalo_alto, label_datos, label_estimacion,flag_filtro

@login_required(login_url='login')
def estimacion_climatica(request,query='mm_lluvia'):
    contexto={}
    try:
        datos_climaticos = Sonda.objects.get(id=150).datos_climaticos_set.all().values('periodo', 'mm_lluvia','temperatura_maxima')
        datos_sonda, datos_prediccion, intervalo_bajo, intervalo_alto,label_datos, label_estimacion,flag_filtro = estimar(datos_climaticos,query)
        contexto["datos_sonda"] = json.dumps(datos_sonda)
        contexto["datos_prediccion"] = json.dumps(datos_prediccion)
        contexto["intervalo_bajo"] = json.dumps(intervalo_bajo)
        contexto["intervalo_alto"] = json.dumps(intervalo_alto)

        contexto["label_datos"] = label_datos
        contexto["label_estimacion"] = label_estimacion

        contexto["flag_filtro"] = flag_filtro

    except Exception as e:
        messages.warning(request,str(e))
    return render(request, "estimacion_climatica.html", contexto)