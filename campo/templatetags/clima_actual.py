from django import template
from datetime import datetime, timedelta 

register = template.Library()

@register.simple_tag
def clima_actual(user):
    campo = user.persona.campo.first()
    return campo.clima_actual()


@register.simple_tag
def yesterday():
    d = datetime.now() - timedelta(days=1)
    return d.strftime('%Y-%m-%d')