from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required":'required'
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "required":'required'
            }
        ))


class RegisterForm(forms.Form):
    documento =  forms.IntegerField(label='Ingresar el documento',
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Documento",
                                                            "required":'required'
                                                            }
                                                        )
                                )

    nombre = forms.CharField(label='Ingresar el nombre',
                                min_length=4,
                                max_length=150,
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Nombre",
                                                            "required":'required'
                                                            }
                                                        )
                                )
    apellido = forms.CharField(label='Ingresar el apellido',
                                min_length=4,
                                max_length=150,
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Apellido",
                                                            "required":'required'
                                                            }
                                                        )
                                )
    fecha_nacimiento = forms.DateField(label='Ingresar fecha nacimiento',
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Fecha Nacimiento"
                                                            }
                                                        )
                                )
    username = forms.CharField(label='Ingresar el nombre de usuario',
                                min_length=4,
                                max_length=150,
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Nombre de usuario",
                                                            "required":'required'
                                                            }
                                                        )
                                )
    email = forms.EmailField(label='Ingresar email',
                            widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "required":'required',
                                                            "placeholder":"Email"
                                                            }
                                                        )
                                )
                            
    password1 = forms.CharField(label='Ingresar contraseña',
                                widget=forms.PasswordInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "required":'required',
                                                            "placeholder":"Contraseña"
                                                            }
                                                        )
                                )
    password2 = forms.CharField(label='Confirmar contraseña', 
                                widget=forms.PasswordInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "required":'required',
                                                            "placeholder":"Confirmacion contraseña"
                                                            }
                                                        )
                                )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("El nombre de usuario ya existe")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email ya existe")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user