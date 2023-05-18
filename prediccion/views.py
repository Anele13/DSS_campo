from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from statsmodels.iolib.smpickle import load_pickle
import pandas as pd
import json
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error

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
    path_csv = staticfiles_storage.path('datos/datos_reducidos_lana.csv')
    modelo_lana = load_pickle(path)
    data = pd.read_csv(path_csv)
    X = data[['cant_lluvia', 'total_ovinos']]
    y = data[['kilos_lana']]
    resultado_prediccion = modelo_lana.predict(X)
    r2 = 'Exactitud de la predicción (R2): {:.2%}'.format(r2_score(y, resultado_prediccion))
    label_estimacion = "Modelo para Estimación de Kg de Lana"
    lana = {
        "title": label_estimacion,
        "metrica": r2,
        "data": json.dumps( {
            "label": [i for i in range(1984, 2023)],
            "y_prediccion": resultado_prediccion.tolist(),
            "y_real": y.kilos_lana.tolist(),
        })
    }
    return lana

def predecir_corderos():
    path = staticfiles_storage.path('data/modelo_prediccion_corderos.pickle')
    path_csv = staticfiles_storage.path('datos/datos_reducidos_corderos.csv')
    modelo_corderos = load_pickle(path)
    data = pd.read_csv(path_csv)
    X = data[['cant_lluvia', 'ovejas']]
    y = data[['cordero/as']]
    resultado_prediccion = modelo_corderos.predict(X)
    r2 = 'Exactitud de la predicción (R2): {:.2%}'.format(r2_score(y, resultado_prediccion))
    label_estimacion = 'Modelo para Estimación de Corderos'
    corderos = {
        "title": label_estimacion,
        "metrica": r2,
        "data": json.dumps( {
            "label": [i for i in range(1984, 2023)],
            "y_prediccion": resultado_prediccion.tolist(),
            "y_real": y['cordero/as'].tolist(),
        })
    }
    return corderos


def predecir_finura():
    path = staticfiles_storage.path('data/modelo_prediccion_lana_finura.pickle')
    path_csv = staticfiles_storage.path('datos/lana_mirabueno_finura.csv')
    modelo_finura = load_pickle(path)
    data = pd.read_csv(path_csv)
    data_finura = data[['fecha', 'finura']]
    steps = 3
    datos_train = data_finura[:-steps]
    datos_test = data_finura[-steps:]
    predicciones = modelo_finura.predict(steps=steps)
    mse = 'Error (MSE): {:.2f} micras'.format(mean_squared_error(datos_test['finura'], predicciones))
    label_estimacion = 'Modelo para Estimación de Finura'
    finura = {
        "title": label_estimacion,
        "metrica": mse,
        "data": json.dumps( {
            "label_prediccion": [2018, 2019, 2020],
            "label_real": build_years(datos_train.fecha),
            "y_prediccion": predicciones.tolist(),
            "y_real": data_finura.finura.tolist(),
        })
    }
    return finura


def predecir_rinde():
    path = staticfiles_storage.path('data/modelo_prediccion_lana_rinde.pickle')
    path_csv = staticfiles_storage.path('datos/lana_mirabueno_rinde.csv')
    modelo_rinde = load_pickle(path)
    steps = 3
    data = pd.read_csv(path_csv)
    data_rinde= data[['fecha', 'rinde']]
    datos_train = data[:-steps]
    datos_test  = data[-steps:]
    prediccion = modelo_rinde.predict(steps=steps)
    mse = 'Error (MSE): {:.2f} rinde'.format(mean_squared_error(datos_test.rinde, prediccion))
    label_estimacion = 'Modelo para Estimación de Rinde'
    rinde = {
        "title": label_estimacion,
        "metrica": mse,
        "data": json.dumps( {
            "label_prediccion": [2018, 2019, 2020],
            "label_real": build_years(datos_train.fecha),
            "y_prediccion": prediccion.tolist(),
            "y_real": data_rinde.rinde.tolist(),
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