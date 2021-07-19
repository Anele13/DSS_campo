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
    documento = forms.IntegerField(label='Ingresar el documento',
                                   widget=forms.TextInput(attrs={
                                       "class": "form-control form-control-user",
                                       "placeholder": "Documento",
                                       "required": 'required'
                                   }
                                   )
                                   )

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
    fecha_nacimiento = forms.DateField(label='Ingresar fecha nacimiento',
                                       widget=forms.DateInput(format=('%d-%m-%Y'), attrs={
                                                              "class": "form-control form-control-user", 'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'})


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
            documento=self.cleaned_data['documento'],
            nombre=self.cleaned_data['nombre'],
            apellido=self.cleaned_data['apellido'],
            fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
            usuario=user
        )

        # Campo
        campo = Campo.objects.create(
            persona=persona,
            sonda=None,
            nombre=self.cleaned_data['nombre_campo'],
            cant_hectareas=self.cleaned_data['cant_hectareas'],
        )
        return user, persona, campo





class UpdateForm(forms.Form):
    documento = forms.IntegerField(label='Ingresar el documento',
                                   widget=forms.TextInput(attrs={
                                       "class": "form-control form-control-user",
                                       "placeholder": "Documento",
                                       "required": 'required'
                                   }
                                   )
                                   )

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
    fecha_nacimiento = forms.DateField(label='Ingresar fecha nacimiento',
                                       widget=forms.DateInput(format=('%d-%m-%Y'), attrs={
                                                              "class": "form-control form-control-user", 'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'})


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

    def clean_cant_hectareas(self):
        cant_hectareas = self.cleaned_data['cant_hectareas']
        if int(cant_hectareas) <= 0:
            raise ValidationError(
                "La cantidad de hectareas debe ser mayor a 0")
        return cant_hectareas

    
    def save(self, user, commit=True):
        # Persona
        persona = user.persona
        if persona:
            persona.documento=self.cleaned_data['documento']
            persona.nombre=self.cleaned_data['nombre']
            persona.apellido=self.cleaned_data['apellido']
            persona.fecha_nacimiento=self.cleaned_data['fecha_nacimiento']
            persona.save()

        else:
            persona = Persona.objects.create(
                documento=self.cleaned_data['documento'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                usuario=user
            )
        
        campo = Campo.objects.get(persona=persona)
        if campo:
            campo.sonda=None
            campo.nombre=self.cleaned_data['nombre_campo']
            campo.cant_hectareas=self.cleaned_data['cant_hectareas']
            campo.save()
        else:
            campo = Campo.objects.create(
                persona=persona,
                sonda=None,
                nombre=self.cleaned_data['nombre_campo'],
                cant_hectareas=self.cleaned_data['cant_hectareas'],
            )
        return user, persona, campo
