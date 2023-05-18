from django.contrib import admin
from usuario.models import User, Persona, TelegramUser, TelegramUrl
# Register your models here.
admin.site.register(Persona)
admin.site.register(TelegramUser)
admin.site.register(TelegramUrl)


