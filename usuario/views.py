from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, UpdateForm
from .models import Persona
from campo.models import Campo
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
import os

from django_telegram_login.widgets.constants import SMALL,MEDIUM, LARGE, DISABLE_USER_PHOTO
from django_telegram_login.widgets.generator import create_redirect_login_widget
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError,TelegramDataIsOutdatedError

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN



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
                form.save()
                return redirect('login')
            else:
                print(form.errors)
        except Exception as e:
            messages.warning(request,'Error:: '+str(e))        
    return render(request, 'registro.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def perfil_view(request):
    user = request.user
    context={}
    if request.GET.get('hash'):
        persona = request.user.persona
        persona.vinculate_telegram_user(request.GET)
    persona, campo = get_persona_campo(user)
    if not (persona and campo):
        return redirect('edicion')
    context['persona']=persona
    context['campo']=campo
    context['telegram_user']=persona.telegramuser_set.all().first()
    context['telegram_url_chat']=f'https://t.me/{bot_name}'
    
    

    from usuario.models import TelegramUrl
    t = TelegramUrl.objects.first()
    redirect_url = None
    if t:
        redirect_url = t.url 
    context['telegram_login_widget']=create_redirect_login_widget(redirect_url, bot_name, size=MEDIUM, user_photo=DISABLE_USER_PHOTO)
    return render(request, 'mi_perfil.html', context)


@login_required(login_url='login')
def editar_perfil_view(request):
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
            datos['nombre']= persona.nombre
            datos['apellido']= persona.apellido
            datos['nombre_campo']= persona.nombre
        if campo:
            datos['nombre_campo']=campo.nombre
            datos['cant_hectareas']=campo.cant_hectareas
            datos['latitud']=campo.latitud
            datos['longitud']=campo.longitud
        form = UpdateForm(initial=datos)
    return render(request, 'editar_perfil.html', {'form': form})


@login_required(login_url='login')
def telegram_users(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        """
        form = UpdateForm(request.POST)
        if form.is_valid():
            form.save(user)
            return redirect('perfil')
        """
    else:
        context['telegram_users'] = user.persona.telegramuser_set.all()
    return render(request, 'telegram_users.html', context)