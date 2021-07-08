from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campo.models import Campo
from produccion.models import DatosProduccion
from produccion.forms import DatosProduccionForm


@login_required(login_url='login')
def cargar_datos_produccion(request):
    contexto={}
    contexto['form'] = DatosProduccionForm()
    campo = Campo.objects.get(persona=request.user.persona)
    if request.method == 'POST':
        if 'archivo_csv' in request.FILES:
            archivo_produccion = request.FILES['archivo_csv']
            try:
                DatosProduccion.agregar_datos_produccion(archivo_produccion, campo)
                messages.success(request,"Datos registrados exitosamente")
            except Exception as e:
                messages.warning(request, str(e))
        else:
            """           
            latitud = request.POST.get('latitud') 
            longitud = request.POST.get('longitud')
            sonda = Sonda.objects.get(latitud=latitud, longitud=longitud)
            campo.sonda=sonda
            campo.save()
            messages.success(request,"Sonda cargada exitosamente")
            """
    return render(request, "alta_datos_produccion.html",contexto)
