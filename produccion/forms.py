from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from .models import DatosProduccion
from django import forms

import datetime


class DatosProduccionForm(forms.Form):

    periodo = forms.DateField(label='Ingresar el año',
                              widget=forms.DateInput(format=('%d-%m-%Y'),
                                                     attrs={
                                  "class": "form-control form-control-user",
                                  "placeholder": "Periodo",
                                  'firstDay': 1,
                                  'pattern=': '\d{4}-\d{2}-\d{2}',
                                  'lang': 'pl',
                                  'format': 'yyyy-mm-dd',
                                  'type': 'date'})
                              )

    cantidad_corderos = forms.IntegerField(label='Ingresar la cantidad de corderos',
                                           widget=forms.TextInput(attrs={
                                               "class": "form-control form-control-user",
                                               "placeholder": "Ingresar la cantidad de corderos",
                                               "required": 'required'
                                           })
                                           )

    cantidad_ovejas = forms.IntegerField(label='Ingresar la cantidad de ovejas',
                                         widget=forms.TextInput(attrs={
                                               "class": "form-control form-control-user",
                                               "placeholder": "Ingresar la cantidad de ovejas",
                                               "required": 'required'
                                         })
                                         )

    cantidad_carneros = forms.IntegerField(label='Ingresar la cantidad de carneros',
                                           widget=forms.TextInput(attrs={
                                               "class": "form-control form-control-user",
                                               "placeholder": "Ingresar la cantidad de carneros",
                                               "required": 'required'
                                           })
                                           )

    cantidad_pariciones = forms.IntegerField(label='Ingresar la cantidad de pariciones',
                                             widget=forms.TextInput(attrs={
                                                 "class": "form-control form-control-user",
                                                 "placeholder": "Ingresar la cantidad de pariciones",
                                                 "required": 'required'
                                             })
                                             )

    cantidad_muertes_corderos = forms.IntegerField(label='Ingresar la cantidad de muertes de corderos',
                                                   widget=forms.TextInput(attrs={
                                                       "class": "form-control form-control-user",
                                                       "placeholder": "Ingresar la mortandad corderos",
                                                       "required": 'required'
                                                   })
                                                   )

    cantidad_lana_producida = forms.IntegerField(label='Ingresar la cantidad de lana producida',
                                                 widget=forms.TextInput(attrs={
                                                     "class": "form-control form-control-user",
                                                     "placeholder": "Ingresar la cantidad de lana producida",
                                                     "required": 'required'
                                                 })
                                                 )

    cantidad_carne_producida = forms.IntegerField(label='Ingresar la cantidad de carne producida',
                                                  widget=forms.TextInput(attrs={
                                                      "class": "form-control form-control-user",
                                                      "placeholder": "Ingresar la cantidad de carne producida",
                                                      "required": 'required'
                                                  })
                                                  )

    rinde_lana = forms.IntegerField(label='Ingresar los rindes',
                                    widget=forms.TextInput(attrs={
                                        "class": "form-control form-control-user",
                                        "placeholder": "Ingresar el rinde de la lana",
                                        "required": 'required'
                                    })
                                    )

    finura_lana = forms.IntegerField(label='Ingresar las finuras',
                                     widget=forms.TextInput(attrs={
                                         "class": "form-control form-control-user",
                                         "placeholder": "Ingresar la finura de la lana",
                                         "required": 'required'
                                     })
                                     )

    def clean_cantidad_corderos(self):
        cantidad_corderos = self.cleaned_data['cantidad_corderos']
        if not isinstance(cantidad_corderos, int):
            raise ValidationError("Debe ingresar un valor númerico")
        if int(cantidad_corderos) <= 0:
            raise ValidationError(
                "La cantidad de corderos no puede ser negativa")
        return cantidad_corderos

    def clean_cantidad_ovejas(self):
        cantidad_ovejas = self.cleaned_data['cantidad_ovejas']
        if int(cantidad_ovejas) <= 0:
            raise ValidationError(
                "La cantidad de ovejas no puede ser negativa")
        return cantidad_ovejas

    def clean_cantidad_carneros(self):
        cantidad_carneros = self.cleaned_data['cantidad_carneros']
        if int(cantidad_carneros) <= 0:
            raise ValidationError(
                "La cantidad de carneros no puede ser negativa")
        return cantidad_carneros

    def clean_cantidad_pariciones(self):
        cantidad_pariciones = self.cleaned_data['cantidad_pariciones']
        if int(cantidad_pariciones) <= 0:
            raise ValidationError(
                "La cantidad de pariciones no puede ser negativa")
        return cantidad_pariciones

    def clean_cantidad_muertes_corderos(self):
        cantidad_muertes_corderos = self.cleaned_data['cantidad_muertes_corderos']
        if int(cantidad_muertes_corderos) <= 0:
            raise ValidationError(
                "La cantidad de muertes de corderos no puede ser negativa")
        return cantidad_muertes_corderos

    def clean_cantidad_lana_producida(self):
        cantidad_lana_producida = self.cleaned_data['cantidad_lana_producida']
        if int(cantidad_lana_producida) <= 0:
            raise ValidationError(
                "La cantidad de lana producida no puede ser negativa")
        return cantidad_lana_producida

    def clean_cantidad_carne_producida(self):
        cantidad_carne_producida = self.cleaned_data['cantidad_carne_producida']
        if int(cantidad_carne_producida) <= 0:
            raise ValidationError(
                "La cantidad de carne producida no puede ser negativa")
        return cantidad_carne_producida

    def clean_rinde_lana(self):
        rinde_lana = self.cleaned_data['rinde_lana']
        if int(rinde_lana) <= 0:
            raise ValidationError(
                "El rinde de la lana no puede ser negativo")
        if int(rinde_lana) > 100:
            raise ValidationError(
                "El rinde de la lana no puede ser mayor a 100")
        return rinde_lana

    def clean_finura_lana(self):
        finura_lana = self.cleaned_data['finura_lana']
        if int(finura_lana) <= 0:
            raise ValidationError(
                "La finura de la lana no puede ser negativa")
        if int(finura_lana) > 100:
            raise ValidationError(
                "La finura de la lana no puede ser mayor a 100")
        return finura_lana
