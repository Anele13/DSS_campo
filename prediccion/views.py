from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from statsmodels.iolib.smpickle import load_pickle
import pandas as pd
import json
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

def transform_data(data_array):
    return [item for lista in data_array.tolist() for item in lista]

def scaler_data(data, modelo, attrs_x, attr_y):
      
    standard_scaler = StandardScaler()

    x_values = data[attrs_x]
    standard_scaler.fit(x_values)
    X_real = standard_scaler.transform(x_values)

    y_values = data[attr_y]
    standard_scaler.fit(y_values)
    y_real = standard_scaler.transform(y_values)

    resultado_prediccion = modelo.predict(X_real)

    y_predicion=standard_scaler.inverse_transform(resultado_prediccion)
    y_real=standard_scaler.inverse_transform(y_real)

    y_prediccion_transform = transform_data(y_predicion)
    y_real_transform = transform_data(y_real)
    r2 = str(round(r2_score(y_real, y_predicion),4) * 100)
    return y_prediccion_transform,y_real_transform,r2

def build_years(fechas):
    anios = []
    for fecha in fechas:
        fecha_partes = fecha.split('-')
        anios.append(int(fecha_partes[0]))
    return anios
    
def predecir_lana():
    path = staticfiles_storage.path('data/modelo_prediccion_lana.pickle')
    path_csv = staticfiles_storage.path('datos/datos_completo_mirabueno.csv')
    modelo_lana = load_pickle(path)
    data = pd.read_csv(path_csv)
    attrs_x = ['cant_lluvia', 'total_ovinos']
    attr_y = ['kilos_lana']
    y_prediccion,y_real,r2 = scaler_data(data, modelo_lana, attrs_x, attr_y)
    anios = build_years(data['fecha'])
    label_estimacion = "Modelo para Estimación de Kg de Lana"
    lana = {
        "title": label_estimacion,
        "metrica": r2,
        "data": json.dumps( {
            "label": anios,
            "y_prediccion": y_prediccion,
            "y_real": y_real,
        })
    }
    return lana

def predecir_corderos():
    path = staticfiles_storage.path('data/modelo_prediccion_corderos.pickle')
    path_csv = staticfiles_storage.path('datos/datos_completo_mirabueno.csv')
    modelo_lana = load_pickle(path)
    data = pd.read_csv(path_csv)
    attrs_x = ['cant_lluvia', 'ovejas']
    attr_y = ['cordero/as']
    y_prediccion,y_real,r2 = scaler_data(data, modelo_lana, attrs_x, attr_y)
    anios = build_years(data['fecha'])
    label_estimacion = 'Modelo para Estimación de Corderos'
    corderos = {
        "title": label_estimacion,
        "metrica": r2,
        "data": json.dumps( {
            "label": anios,
            "y_prediccion": y_prediccion,
            "y_real": y_real,
        })
    }
    return corderos

def predecir_finura():
    path = staticfiles_storage.path('data/modelo_prediccion_lana_finura.pickle')
    path_csv = staticfiles_storage.path('datos/datos_completo_mirabueno.csv')
    modelo_finura = load_pickle(path)
    data = pd.read_csv(path_csv)
    data_finura = data[['fecha', 'finura']]
    steps = 3
    prediccion = modelo_finura.predict(steps=steps)
    data_prediccion = pd.DataFrame({'fecha':prediccion.index, 'finura':prediccion.values})
    anios_real = build_years(data_finura['fecha'])
    anios_prediccion = [2020,2021,2022]
    y_prediccion = data_prediccion.finura.tolist()
    y_real = data_finura.finura.tolist()
    r2 = str(round(r2_score(y_real[:3], y_prediccion),4) * 100)
    label_estimacion = 'Modelo para Estimación de Finura'
    finura = {
        "title": label_estimacion,
        "metrica": r2,
        "data": json.dumps( {
            "label_prediccion": anios_prediccion,
            "label_real": anios_real,
            "y_prediccion": y_prediccion,
            "y_real": y_real,
        })
    }
    return finura

def predecir_rinde():
    path = staticfiles_storage.path('data/modelo_prediccion_lana_rinde.pickle')
    path_csv = staticfiles_storage.path('datos/datos_completo_mirabueno.csv')
    modelo_rinde = load_pickle(path)
    data = pd.read_csv(path_csv)
    data_rinde= data[['fecha', 'rinde']]
    steps = 3
    prediccion = modelo_rinde.predict(steps=steps)
    data_prediccion = pd.DataFrame({'fecha':prediccion.index, 'rinde':prediccion.values})
    anios_real = build_years(data_rinde['fecha'])
    anios_prediccion = [2020,2021,2022]
    y_prediccion = data_prediccion.rinde.tolist()
    y_real = data_rinde.rinde.tolist()
    r2 = str(round(r2_score(y_real[:3], y_prediccion),4) * 100)
    label_estimacion = 'Modelo para Estimación de Rinde'
    rinde = {
        "title": label_estimacion,
        "metrica": r2,
        "data": json.dumps( {
            "label_prediccion": anios_prediccion,
            "label_real": anios_real,
            "y_prediccion": y_prediccion,
            "y_real": y_real,
        })
    }
    return rinde

@login_required(login_url='login')
def predecir(request):
    datos_lana = predecir_lana()
    datos_corderos = predecir_corderos()
    datos_finura = predecir_finura()
    datos_rinde = predecir_rinde()
    
    contexto = {}
    
    contexto["lana"] = datos_lana
    contexto["corderos"] = datos_corderos
    contexto["finura"] = datos_finura
    contexto["rinde"] = datos_rinde

    return render(request, "prediccion.html", contexto)