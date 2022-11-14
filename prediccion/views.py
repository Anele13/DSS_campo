from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def prediccion_lana(request):
    contexto = {
        'msg':'Hola'
    }
    return render(request, "prediccion.html", contexto)
