from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import pandas as pd
from .models import DatosClimaticos, Sonda
from campo.models import Campo
from usuario.models import Persona
from usuario.views import get_persona_campo
import json


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



@login_required(login_url='login')
def estimacion_climatica(request):
    cosa = [{"x":"2010-01-01", "y": 0.35806451612903223},
            {"x":"2010-02-01", "y": 1.45},
            {"x":"2010-03-01", "y": 0.041935483870967745},
            {"x":"2010-04-01", "y": 0.1},
            {"x":"2010-05-01", "y": 0.3516129032258064},
            {"x":"2010-06-01", "y": 3.3566666666666665},
            {"x":"2010-07-01", "y": 2.025806451612903},
            {"x":"2010-08-01", "y": 0.8516129032258064},
            {"x":"2010-09-01", "y": 0.12000000000000001},
            {"x":"2010-10-01", "y": 0.09999999999999999},
            {"x":"2010-11-01", "y": 0.2533333333333333},
            {"x":"2010-12-01", "y": 0.3419354838709678},
            {"x":"2011-01-01", "y": 0.27096774193548384},
            {"x":"2011-02-01", "y": 0.6928571428571428},
            {"x":"2011-03-01", "y": 0.5161290322580645},
            {"x":"2011-04-01", "y": 0.8333333333333334},
            {"x":"2011-05-01", "y": 0.13548387096774195},
            {"x":"2011-06-01", "y": 0.22},
            {"x":"2011-07-01", "y": 0.9548387096774192},
            {"x":"2011-08-01", "y": 0.6000000000000001},
            {"x":"2011-09-01", "y": 0.04666666666666666},
            {"x":"2011-10-01", "y": 0.40645161290322585},
            {"x":"2011-11-01", "y": 0.14},
            {"x":"2011-12-01", "y": 0.0},
            {"x":"2012-01-01", "y": 0.8580645161290322},
            {"x":"2012-02-01", "y": 0.606896551724138},
            {"x":"2012-03-01", "y": 0.3806451612903226},
            {"x":"2012-04-01", "y": 0.18666666666666668},
            {"x":"2012-05-01", "y": 1.6451612903225807},
            {"x":"2012-06-01", "y": 1.5733333333333337},
            {"x":"2012-07-01", "y": 0.2838709677419355},
            {"x":"2012-08-01", "y": 0.8516129032258064},
            {"x":"2012-09-01", "y": 0.14},
            {"x":"2012-10-01", "y": 0.18064516129032257},
            {"x":"2012-11-01", "y": 0.3333333333333333},
            {"x":"2012-12-01", "y": 0.37419354838709673},
            {"x":"2013-01-01", "y": 0.10967741935483871},
            {"x":"2013-02-01", "y": 0.49999999999999994},
            {"x":"2013-03-01", "y": 0.14838709677419354},
            {"x":"2013-04-01", "y": 0.006666666666666667},
            {"x":"2013-05-01", "y": 0.8451612903225806},
            {"x":"2013-06-01", "y": 0.5333333333333333},
            {"x":"2013-07-01", "y": 0.6193548387096773},
            {"x":"2013-08-01", "y": 0.3677419354838709},
            {"x":"2013-09-01", "y": 0.5},
            {"x":"2013-10-01", "y": 0.0},
            {"x":"2013-11-01", "y": 0.14},
            {"x":"2013-12-01", "y": 0.0},
            {"x":"2014-01-01", "y": 0.09032258064516129},
            {"x":"2014-02-01", "y": 0.0},
            {"x":"2014-03-01", "y": 0.12903225806451613},
            {"x":"2014-04-01", "y": 0.25333333333333335},
            {"x":"2014-05-01", "y": 1.6709677419354838},
            {"x":"2014-06-01", "y": 1.0533333333333332},
            {"x":"2014-07-01", "y": 0.45806451612903215},
            {"x":"2014-08-01", "y": 1.6903225806451612},
            {"x":"2014-09-01", "y": 1.1600000000000001},
            {"x":"2014-10-01", "y": 0.2709677419354839},
            {"x":"2014-11-01", "y": 0.26666666666666666},
            {"x":"2014-12-01", "y": 0.4580645161290323},
            {"x":"2015-01-01", "y": 0.07741935483870968},
            {"x":"2015-02-01", "y": 0.13571428571428573},
            {"x":"2015-03-01", "y": 0.6709677419354839},
            {"x":"2015-04-01", "y": 0.8333333333333333},
            {"x":"2015-05-01", "y": 1.4645161290322586},
            {"x":"2015-06-01", "y": 0.5533333333333332},
            {"x":"2015-07-01", "y": 0.6451612903225806},
            {"x":"2015-08-01", "y": 0.5354838709677419},
            {"x":"2015-09-01", "y": 0.04666666666666666},
            {"x":"2015-10-01", "y": 0.0774193548387097},
            {"x":"2015-11-01", "y": 0.03333333333333333},
            {"x":"2015-12-01", "y": 0.06451612903225806},
            {"x":"2016-01-01", "y": 0.2225806451612903},
            {"x":"2016-02-01", "y": 0.4827586206896552},
            {"x":"2016-03-01", "y": 0.7806451612903227},
            {"x":"2016-04-01", "y": 0.14666666666666664},
            {"x":"2016-05-01", "y": 0.2838709677419355},
            {"x":"2016-06-01", "y": 0.44000000000000017},
            {"x":"2016-07-01", "y": 0.09677419354838711},
            {"x":"2016-08-01", "y": 0.6387096774193549},
            {"x":"2016-09-01", "y": 0.5700000000000001},
            {"x":"2016-10-01", "y": 0.3032258064516129},
            {"x":"2016-11-01", "y": 0.4800000000000001},
            {"x":"2016-12-01", "y": 0.5838709677419355},
            {"x":"2017-01-01", "y": 0.25806451612903225},
            {"x":"2017-02-01", "y": 0.34285714285714286},
            {"x":"2017-03-01", "y": 0.6774193548387096},
            {"x":"2017-04-01", "y": 0.9999999999999999},
            {"x":"2017-05-01", "y": 0.6451612903225805},
            {"x":"2017-06-01", "y": 1.26},
            {"x":"2017-07-01", "y": 0.7032258064516129},
            {"x":"2017-08-01", "y": 0.6451612903225805},
            {"x":"2017-09-01", "y": 0.32},
            {"x":"2017-10-01", "y": 0.14838709677419354},
            {"x":"2017-11-01", "y": 0.04000000000000001},
            {"x":"2017-12-01", "y": 0.19354838709677416},
            {"x":"2018-01-01", "y": 0.0064516129032258064},
            {"x":"2018-02-01", "y": 0.03571428571428571},
            {"x":"2018-03-01", "y": 0.21935483870967742},
            {"x":"2018-04-01", "y": 0.6799999999999999},
            {"x":"2018-05-01", "y": 0.5032258064516129},
            {"x":"2018-06-01", "y": 0.8333333333333334},
            {"x":"2018-07-01", "y": 0.5870967741935484},
            {"x":"2018-08-01", "y": 0.23225806451612904},
            {"x":"2018-09-01", "y": 1.0},
            {"x":"2018-10-01", "y": 0.03225806451612903},
            {"x":"2018-11-01", "y": 0.58},
            {"x":"2018-12-01", "y": 0.0064516129032258064},
            {"x":"2019-01-01", "y": 0.03870967741935484},
            {"x":"2019-02-01", "y": 0.0071428571428571435},
            {"x":"2019-03-01", "y": 0.42580645161290315},
            {"x":"2019-04-01", "y": 0.45333333333333337},
            {"x":"2019-05-01", "y": 0.44516129032258067},
            {"x":"2019-06-01", "y": 0.7866666666666666},
            {"x":"2019-07-01", "y": 0.6064516129032258},
            {"x":"2019-08-01", "y": 0.4645161290322581},
            {"x":"2019-09-01", "y": 0.0},
            {"x":"2019-10-01", "y": 0.1935483870967742},
            {"x":"2019-11-01", "y": 0.49333333333333335},
            {"x":"2019-12-01", "y": 0.17419354838709677},
            {"x":"2020-01-01", "y": 0.03870967741935484},
            {"x":"2020-02-01", "y": 0.4482758620689655},
            {"x":"2020-03-01", "y": 0.06451612903225806},
            {"x":"2020-04-01", "y": 0.3933333333333333},
            {"x":"2020-05-01", "y": 0.7354838709677418},
            {"x":"2020-06-01", "y": 1.6666666666666672},
            {"x":"2020-07-01", "y": 2.103225806451613},
            {"x":"2020-08-01", "y": 0.3354838709677419},
            {"x":"2020-09-01", "y": 0.3133333333333333},
            {"x":"2020-10-01", "y": 0.23225806451612904},
            {"x":"2020-11-01", "y": 0.04},
            {"x":"2020-12-01", "y": 0.03870967741935484}]   

    cosa2 = [{"x":'2021-01-01', "y": 0.06752939188815746},
            {"x":'2021-02-01',"y": 0.2590946227812676},
            {"x":'2021-03-01',"y": 0.30222466623751865},
            {"x":'2021-04-01',"y": 0.49778176819756836},
            {"x":'2021-05-01',"y": 0.6524669199619846},
            {"x":'2021-06-01',"y": 1.15468207817146,'u':8, 'd':10},
            {"x":'2021-07-01',"y": 1.1402641823102093,'u':10, 'd':10},
            {"x":'2021-08-01',"y": 0.4474095313121122,'u':15, 'd':10},
            {"x":'2021-09-01',"y": 0.3651777133354068,'u':20, 'd':10},
            {"x":'2021-10-01',"y": 0.18176169850017002,'u':4, 'd':10}]



    intervalo_bajo =[{"x":'2021-01-01',"y": -0.7392854918494568},
                    {"x":'2021-02-01',"y": -0.5632382377380326},
                    {"x":'2021-03-01',"y": -0.5200936423651265},
                    {"x":'2021-04-01',"y": -0.32453654040507673},
                    {"x":'2021-05-01',"y": -0.16985138864066052},
                    {"x":'2021-06-01',"y": 0.33236376956881486},
                    {"x":'2021-07-01',"y": 0.3179458737075642},
                    {"x":'2021-08-01',"y": -0.3749087772905328},
                    {"x":'2021-09-01',"y": -0.4571405952672383},
                    {"x":'2021-10-01',"y": -0.6405566101024751}]

    intervalo_alto = [{"x":'2021-01-01', "y": 0.8743442756257717},
                    {"x":'2021-02-01', "y": 1.0814274833005677},
                    {"x":'2021-03-01', "y": 1.1245429748401636},
                    {"x":'2021-04-01', "y": 1.3201000768002134},
                    {"x":'2021-05-01', "y": 1.4747852285646297},
                    {"x":'2021-06-01', "y": 1.977000386774105},
                    {"x":'2021-07-01', "y": 1.9625824909128544},
                    {"x":'2021-08-01', "y": 1.2697278399147571},
                    {"x":'2021-09-01', "y": 1.187496021938052},
                    {"x":'2021-10-01', "y": 1.004080007102815}]


    contexto={}
    contexto["datos_sonda"] = json.dumps(cosa)
    contexto["datos_prediccion"] = json.dumps(cosa2)

    contexto["intervalo_bajo"] = json.dumps(intervalo_bajo)
    contexto["intervalo_alto"] = json.dumps(intervalo_alto)
    return render(request, "estimacion_climatica.html", contexto)