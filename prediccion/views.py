from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from statsmodels.iolib.smpickle import load_pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import json


def predecir_lana():
    path = staticfiles_storage.path('data/modelo_prediccion_lana.pickle')
    modelo_lana = load_pickle(path)
    path_csv = staticfiles_storage.path('datos/datos_completo_mirabueno.csv')
    data = pd.read_csv(path_csv)
    num_attrs = ["cant_lluvia", "total_ovinos"]
    pipeline = ColumnTransformer([("numeric", StandardScaler(), num_attrs)])
    X_prediccion = pipeline.fit_transform(data)
    standard_scaler = StandardScaler()
    l_values = data[['kilos_lana']]
    scaled_values = standard_scaler.fit(l_values)
    y_prediccion = standard_scaler.transform(l_values)
    resultado_prediccion_mirabueno_scaler = modelo_lana.predict(X_prediccion)
    y_predición_kg=standard_scaler.inverse_transform(resultado_prediccion_mirabueno_scaler)
    y_real_kg=standard_scaler.inverse_transform(y_prediccion)
    anios = []
    for fecha in data['fecha']:
        fecha_partes = fecha.split('-')
        anios.append(fecha_partes[0])
    label_datos = 'Lluvia Observada'
    label_estimacion = 'Estimación de Lluvia'
    flag_filtro = "Mm de Lluvia Anuales"
    return anios, y_predición_kg, y_real_kg

def predecir_por_filtro(filtro):
    label_estimacion = None
    label_datos = None
    flag_filtro = None
    if filtro == 'lana':
        print('Lanaa')
        anios, y_predición_kg, y_real_kg = predecir_lana()
        label_datos = 'Kgs de lana Observada'
        label_estimacion = 'Estimación de Producción de lana'
        flag_filtro = 'Kg de lana'
    elif filtro== 'corderos':
        print('Corderos')
        flag_filtro = 'Cantidad de corderos'
    return label_estimacion, label_datos, flag_filtro, anios, y_predición_kg, y_real_kg

@login_required(login_url='login')
def predecir(request,query='lana'):
    label_datos, label_estimacion, flag_filtro, anios, y_predición_kg, y_real_kg = predecir_por_filtro(query)
    contexto = {}
    contexto["label_datos"] = label_datos
    contexto["label_estimacion"] = label_estimacion
    contexto["flag_filtro"] = flag_filtro
    contexto["anios"] = anios
    contexto["y_predición_kg"] = y_predición_kg
    contexto["y_real_kg"] = y_real_kg
    return render(request, "prediccion.html", contexto)

'''
  // var y_predición_kg = {{y_predición_kg|safe}}
  //var y_real_kg = {{y_real_kg|safe}}
'''
