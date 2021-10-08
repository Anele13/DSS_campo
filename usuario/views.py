from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, UpdateForm
from .models import Persona
from django.contrib.auth.models import User
from campo.models import Campo
from django.contrib import messages
from datetime import datetime

def get_persona_campo(user):
    persona = None
    campo = None
    try:
        persona = Persona.objects.get(usuario=user)
    except Exception as e:
        pass
    try:
        campo = Campo.objects.get(persona=persona)
    except Exception:
        pass
    return persona, campo


def login_view(request):
    form = LoginForm()
    msg = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('inicio')
            else:
                messages.warning(request,'Credenciales inválidas')
    return render(request, "login.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect('login')


def registro(request):
    form = RegisterForm()
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():
                usuario = form.save()
                return redirect('login')
        except Exception as e:
            messages.warning(request,'Error:: '+str(e))        
    return render(request, 'registro.html', {'form': form})


def perfil_view(request):
    contexto = {}
    user = request.user
    persona, campo = get_persona_campo(user)
    if not (persona and campo):
        return redirect('edicion')
    return render(request, 'mi_perfil.html', {'persona': persona, 'campo': campo})


def editar_perfil_view(request):
    contexto = {}
    user = request.user
    datos = {}
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('perfil')
    else:
        persona, campo = get_persona_campo(user)
        if persona:
            datos['documento']= persona.documento
            datos['nombre']= persona.nombre
            datos['apellido']= persona.apellido
            datos['fecha_nacimiento']= persona.fecha_nacimiento.strftime('%Y-%m-%d')
            datos['nombre_campo']= persona.nombre
        if campo:
            datos['nombre_campo']=campo.nombre
            datos['cant_hectareas']=campo.cant_hectareas
        form = UpdateForm(initial=datos)
    return render(request, 'editar_perfil.html', {'form': form})
