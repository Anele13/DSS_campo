from django import template

register = template.Library()

@register.simple_tag
def clima_actual(user):
    campo = user.persona.campo.first()
    return campo.clima_actual()