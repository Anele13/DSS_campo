from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from campo.models import Campo
from usuario.models import Persona


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": 'required'
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required": 'required'
            }
        ))


class RegisterForm(forms.Form):
    nombre = forms.CharField(label='Ingresar el nombre',
                             min_length=4,
                             max_length=150,
                             widget=forms.TextInput(attrs={
                                 "class": "form-control form-control-user",
                                 "placeholder": "Nombre",
                                 "required": 'required'
                             }
                             )
                             )
    apellido = forms.CharField(label='Ingresar el apellido',
                               min_length=4,
                               max_length=150,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control form-control-user",
                                   "placeholder": "Apellido",
                                   "required": 'required'
                               }
                               )
                               )

    username = forms.CharField(label='Ingresar el nombre de usuario',
                               min_length=4,
                               max_length=150,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control form-control-user",
                                   "placeholder": "Nombre de usuario",
                                   "required": 'required'
                               }
                               )
                               )
    email = forms.EmailField(label='Ingresar email',
                             widget=forms.TextInput(attrs={
                                 "class": "form-control form-control-user",
                                 "required": 'required',
                                 "placeholder": "Email"
                             }
                             )
                             )

    password1 = forms.CharField(label='Ingresar contraseña',
                                widget=forms.PasswordInput(attrs={
                                    "class": "form-control form-control-user",
                                    "required": 'required',
                                    "placeholder": "Contraseña"
                                }
                                )
                                )
    password2 = forms.CharField(label='Confirmar contraseña',
                                widget=forms.PasswordInput(attrs={
                                    "class": "form-control form-control-user",
                                    "required": 'required',
                                    "placeholder": "Confirmacion contraseña"
                                }
                                )
                                )

    cant_hectareas = forms.IntegerField(label='Ingresar el la cantidad de hectareas',
                                        widget=forms.TextInput(attrs={
                                            "class": "form-control form-control-user",
                                            "placeholder": "Cantidad de Hectareas",
                                            "required": 'required'
                                        }
                                        )
                                        )

    nombre_campo = forms.CharField(label='Ingresar el nombre',
                                   min_length=4,
                                   max_length=150,
                                   widget=forms.TextInput(attrs={
                                       "class": "form-control form-control-user",
                                       "placeholder": "Nombre del Campo",
                                       "required": 'required'
                                   }
                                   )
                                   )

    latitud =  forms.FloatField(label='Latitud',
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Latitud",
                                                            "required":'required'
                                                            }
                                                        )
                                )

    longitud = forms.FloatField(label='Longitud',
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Longitud",
                                                            "required":'required'
                                                            }
                                                        )
                                )

    def clean_cant_hectareas(self):
        cant_hectareas = self.cleaned_data['cant_hectareas']
        if int(cant_hectareas) <= 0:
            raise ValidationError(
                "La cantidad de hectareas debe ser mayor a 0")
        return cant_hectareas

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email ya existe")
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")
        return password2


    def save(self, crear_usuario=True):
        # Usuario
        if crear_usuario:
            user = User.objects.create_user(
                self.cleaned_data['username'],
                self.cleaned_data['email'],
                self.cleaned_data['password1']
            )

        # Persona
        persona = Persona.objects.create(
            nombre=self.cleaned_data['nombre'],
            apellido=self.cleaned_data['apellido'],
            usuario=user
        )

        # Campo
        campo = Campo.objects.create(
            persona=persona,
            nombre=self.cleaned_data['nombre_campo'],
            cant_hectareas=self.cleaned_data['cant_hectareas'],
            latitud=self.cleaned_data['latitud'],
            longitud=self.cleaned_data['longitud'],
        )

        campo.create_in_firebase()
        return user, persona, campo


class UpdateForm(forms.Form):
    nombre = forms.CharField(label='Ingresar el nombre',
                             min_length=4,
                             max_length=150,
                             widget=forms.TextInput(attrs={
                                 "class": "form-control form-control-user",
                                 "placeholder": "Nombre",
                                 "required": 'required'
                             }
                             )
                             )
    apellido = forms.CharField(label='Ingresar el apellido',
                               min_length=4,
                               max_length=150,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control form-control-user",
                                   "placeholder": "Apellido",
                                   "required": 'required'
                               }
                               )
                               )
    cant_hectareas = forms.IntegerField(label='Ingresar el la cantidad de hectareas',
                                        widget=forms.TextInput(attrs={
                                            "class": "form-control form-control-user",
                                            "placeholder": "Cantidad de Hectareas",
                                            "required": 'required'
                                        }
                                        )
                                        )

    nombre_campo = forms.CharField(label='Ingresar el nombre',
                                   min_length=4,
                                   max_length=150,
                                   widget=forms.TextInput(attrs={
                                       "class": "form-control form-control-user",
                                       "placeholder": "Nombre del Campo",
                                       "required": 'required'
                                   }
                                   )
                                   )

    latitud =  forms.FloatField(label='Latitud',
                                widget=forms.NumberInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Latitud",
                                                            "required":'required'
                                                            })) 

    longitud = forms.FloatField(label='Longitud',
                                widget=forms.NumberInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Latitud",
                                                            "required":'required'
                                                            })) 

    def clean_cant_hectareas(self):
        cant_hectareas = self.cleaned_data['cant_hectareas']
        if int(cant_hectareas) <= 0:
            raise ValidationError(
                "La cantidad de hectareas debe ser mayor a 0")
        return cant_hectareas

    
    def save(self, user, commit=True):
        # Persona
        try:
            persona = Persona.objects.get(usuario=user)
        except Exception:
            persona = None

        if persona:
            persona.nombre=self.cleaned_data['nombre']
            persona.apellido=self.cleaned_data['apellido']
            persona.save()

        else:
            persona = Persona.objects.create(
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                usuario=user
            )
        
        try:
            campo = Campo.objects.get(persona=persona)
        except Exception:
            campo = None
            
        if campo:
            campo.nombre=self.cleaned_data['nombre_campo']
            campo.cant_hectareas=self.cleaned_data['cant_hectareas']
            data1 = self.cleaned_data['latitud']
            data2 = self.cleaned_data['longitud']
            campo.latitud=data1
            campo.longitud=data2
            campo.save()
        else:
            campo = Campo.objects.create(
                persona=persona,
                nombre=self.cleaned_data['nombre_campo'],
                cant_hectareas=self.cleaned_data['cant_hectareas'],
                latitud=self.cleaned_data['latitud'],
                longitud=self.cleaned_data['longitud'],
            )
        return user, persona, campo
