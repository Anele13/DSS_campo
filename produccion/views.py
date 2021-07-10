from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campo.models import Campo
from produccion.models import DatosProduccion
from produccion.forms import DatosProduccionForm
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required(login_url='login')
def cargar_datos_produccion(request):
    contexto = {}
    campo = Campo.objects.get(persona=request.user.persona)
    if request.method == 'POST':
        if 'archivo_csv' in request.FILES:
            archivo_produccion = request.FILES['archivo_csv']
            try:
                DatosProduccion.agregar_datos_produccion(
                    archivo_produccion, campo)
                messages.success(request, "Datos registrados exitosamente")
                contexto['form'] = DatosProduccionForm()
            except Exception as e:
                messages.warning(request, str(e))
        else:
            form = DatosProduccionForm(request.POST)
            if form.is_valid():
                datos_produccion = DatosProduccion()
                datos_produccion.periodo = form.cleaned_data["periodo"]
                datos_produccion.cantidad_corderos = form.clean_cantidad_corderos()
                datos_produccion.cantidad_carneros = form.clean_cantidad_carneros()
                datos_produccion.cantidad_carne_producida = form.clean_cantidad_carne_producida()
                datos_produccion.cantidad_lana_producida = form.clean_cantidad_lana_producida()
                datos_produccion.cantidad_muertes_corderos = form.clean_cantidad_muertes_corderos()
                datos_produccion.cantidad_ovejas = form.clean_cantidad_ovejas()
                datos_produccion.cantidad_pariciones = form.clean_cantidad_pariciones()
                datos_produccion.rinde_lana = form.clean_rinde_lana()
                datos_produccion.finura_lana = form.clean_finura_lana()
                datos_produccion.campo = campo
                datos_produccion.save()
                messages.success(request, "Datos registrados exitosamente")
                return HttpResponseRedirect(reverse("carga_datos_produccion"))
            else:
                print("NO ES")
                print(form.errors)
                contexto['form'] = form
    else:
        contexto['form'] = DatosProduccionForm()
    return render(request, "alta_datos_produccion.html", contexto)
