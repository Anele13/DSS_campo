from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campo.models import Campo
from produccion.models import DatosProduccion
from produccion.forms import DatosProduccionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from usuario.views import get_persona_campo


@login_required(login_url='login')
def cargar_datos_produccion(request):
    contexto = {}
    user = request.user
    if request.method == 'POST':
        try:
            campo = Campo.objects.get(persona=request.user.persona)
            contexto['formulario_produccion'] = DatosProduccionForm()
            if 'archivo_csv' in request.FILES:
                archivo_produccion = request.FILES['archivo_csv']
                DatosProduccion.agregar_datos_produccion(archivo_produccion, campo)
                messages.success(request, "Datos registrados exitosamente")
            else:
                form = DatosProduccionForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Datos registrados exitosamente")
        except Exception as e:
            messages.warning(request, str(e))
    else:
        persona, campo = get_persona_campo(user)
        if not (persona and campo):
            messages.warning(request, "Cargue sus datos personales y de su campo.")
        else:
            contexto['formulario_produccion'] = DatosProduccionForm()
    return render(request, "alta_datos_produccion.html", contexto)
