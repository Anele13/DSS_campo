from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DatosProduccionForm


@login_required(login_url='login')
def cargar_datos_produccion(request):
    form = DatosProduccionForm()
    contexto = {
        'form': form
    }

    if request.method == 'POST':
        print("Hollaaaaa 1")
        if 'archivo_csv' in request.FILES:
            print("Hollaaaaa 2")
            archivo_climatico = request.FILES['archivo_csv']
            try:
                messages.success(request, 'Alta de datos correcta!')
            except Exception as e:
                messages.warning(request, str(e))
        else:
            form = DatosProduccionForm(request.POST)
            print("Hollaaaaa 3")
            return render(request, "alta_datos_produccion.html", {'form': form})

    return render(request, "alta_datos_produccion.html", contexto)
