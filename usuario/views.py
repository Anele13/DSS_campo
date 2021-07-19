from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, UpdateForm
from .models import Persona
from django.contrib.auth.models import User
from campo.models import Campo


def login_view(request):
    msg = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('inicio')
            else:
                msg = 'Credenciales invalidas'
        else:
            msg = 'Error en los datos ingresados'
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect('login')


def registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'registro.html', {'form': form})


def perfil_view(request):
    contexto = {}
    datos_persona = Persona.objects.get(usuario=request.user)
    datos_campo = Campo.objects.get(persona=datos_persona)
    return render(request, 'mi_perfil.html', {'usuario': datos_persona, 'campo': datos_campo})


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
        if user.persona:
            p = user.persona
            datos['documento']= p.documento
            datos['nombre']= p.nombre
            datos['apellido']= p.apellido
            datos['fecha_nacimiento']= p.fecha_nacimiento
            datos['nombre_campo']= p.nombre
        campo = Campo.objects.get(persona=request.user.persona)
        if campo:
            datos['nombre_campo']=campo.nombre
            datos['cant_hectareas']=campo.cant_hectareas
        form = UpdateForm(initial=datos)
    return render(request, 'editar_perfil.html', {'form': form})
