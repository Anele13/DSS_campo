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


@login_required(login_url='login')
def estimacion_climatica(request):
    try:
        datos_climaticos = Sonda.objects.get(id=150).datos_climaticos_set.all().values('periodo', 'mm_lluvia')
        df = pd.DataFrame(datos_climaticos)
        df[['periodo']] = pd.to_datetime(df['periodo'])
        df.set_index('periodo',inplace=True)
        df.index.name = None
        df = df['mm_lluvia'].resample('MS').mean()
        df = df.fillna(df.bfill())

        #cargo el modelo entrenado
        path = staticfiles_storage.path('data/modelo.pickle')
        results = load_pickle(path)

        #datos originales
        datos_sonda = format(df.to_dict())

        #estimacion climatica
        pred_uc = results.get_forecast(steps=10)
        datos_prediccion = format(pred_uc.predicted_mean.to_dict())

        #intervalos de confianza
        pred_ci = pred_uc.conf_int()
        intervalo_bajo = format(pred_ci[['lower mm_lluvia']].to_dict()['lower mm_lluvia'])
        intervalo_alto =format(pred_ci[['upper mm_lluvia']].to_dict()['upper mm_lluvia'])

        
        contexto={}
        contexto["datos_sonda"] = json.dumps(datos_sonda)
        contexto["datos_prediccion"] = json.dumps(datos_prediccion)
        contexto["intervalo_bajo"] = json.dumps(intervalo_bajo)
        contexto["intervalo_alto"] = json.dumps(intervalo_alto)
    except Exception as e:
        messages.warning(request,str(e))
    return render(request, "estimacion_climatica.html", contexto)