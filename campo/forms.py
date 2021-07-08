from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AltaCampoForm(forms.Form):
    cant_hectareas =  forms.IntegerField(label='Ingresar el la cantidad de hectareas',
                                widget=forms.TextInput(attrs={
                                                            "class": "form-control form-control-user",
                                                            "placeholder":"Cantidad de Hectareas",
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
    
    def clean_cant_hectareas(self):
        cant_hectareas = self.cleaned_data['cant_hectareas'].lower()
        if int(cant_hectareas) < 0:
            raise  ValidationError("La cantidad de hectareas debe ser mayor a 0")
        return cant_hectareas

   
    def save(self, persona, commit=True):
        campo = Campo.objects.create(
            persona,
            None,
            self.cleaned_data['nombre'],
            self.cleaned_data['cant_hectareas'],
        )   
        return campo