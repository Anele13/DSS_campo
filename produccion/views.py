from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='login')
def cargar_datos_produccion(request):
    contexto={}
    if request.method == 'POST':
        messages.success(request, 'Alta de datos correcta!')
    return render(request, "alta_datos_produccion.html",contexto)
