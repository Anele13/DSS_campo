from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from sqlalchemy import create_engine
import pandas as pd
from .models import DatosClimaticos, Sonda
from sistema_campo.settings import BASE_DIR
@login_required(login_url='login')
def cargar_datos_climaticos(request):
    contexto={}
    #Deben ser mas sondas pero luego sacamos mas..
    c = Sonda.objects.all()
    sondas = {}
    for a in c:
        if a.latitud and a.longitud:
            sondas[str(a.id)] = {'nombre':a.nombre,
                            'latitud':a.latitud,
                            'longitud':a.longitud,
                            'altura': 0}
    contexto['sondas'] = json.dumps(sondas)
    if request.method == 'POST':
        messages.success(request, 'Alta de datos correcta!')
        #engine = create_engine('sqlite://'+BASE_DIR.as_posix()+'/db.sqlite3', echo=False)
        archivo = request.FILES['archivo_csv']
        if archivo:
            df = pd.read_csv(archivo)
            #df.to_sql('clima_datosclimaticos', con=engine, if_exists='append')
          
    return render(request, "alta_datos_climaticos.html",contexto)
