from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from .models import Persona
from django.contrib.auth.models import User
from campo.models import Campo
from django.shortcuts import get_object_or_404


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
    usuario = request.user
    usu = User.objects.get(username=usuario)
    datos_persona = Persona.objects.get(usuario=usuario)
    datos_campo = Campo.objects.get(persona=datos_persona)

    return render(request, 'mi_perfil.html', {'usuario': datos_persona, 'campo': datos_campo, 'userId': usu.id})


def editar_perfil_view(request, pk):
    contexto = {}
    usuario_inst = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save(crear_usuario=False)
            return redirect('miperfil')
        else:
            print(form.errors)
    else:
        datos = Persona.objects.get(usuario=usuario_inst)
        datos_campo = Campo.objects.get(persona=datos)
        datos_2 = {'documento': datos.documento,
                   'nombre': datos.nombre,
                   'apellido': datos.apellido,
                   'fecha_nacimiento': datos.fecha_nacimiento,
                   'nombre_campo': datos_campo.nombre,
                   'cant_hectareas': datos_campo.cant_hectareas,
                   }
        # form = RegisterForm(instance=datos_2) no anda porque no es un ModelForms
        form = RegisterForm(initial=datos_2)
        ''' form = RegisterForm(datos_2, initial=datos_2)
            if form.has_changed():
            form.save()'''

    return render(request, 'editar_perfil.html', {'form': form, 'userId': usuario_inst.id})
