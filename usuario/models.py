from django.db import models
from django.contrib.auth.models import User
import os

from django_telegram_login.widgets.constants import SMALL,MEDIUM, LARGE, DISABLE_USER_PHOTO
from django_telegram_login.widgets.generator import create_redirect_login_widget
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError,TelegramDataIsOutdatedError
from django.conf import settings

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN

class Persona(models.Model):
    nombre = models.CharField(max_length=30, blank=True, null=True)
    apellido = models.CharField(max_length=30, blank=True, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')

    def vinculate_telegram_user(self, data):
        telegram_user = None
        try:
            result = verify_telegram_authentication(bot_token=bot_token, request_data=data)
            if result and not TelegramUser.objects.filter(id=result['id']).exists():
                user_data = result.dict()
                user_data.update({'persona':self})
                telegram_user = TelegramUser.objects.create(**user_data)
        except TelegramDataIsOutdatedError:
            pass #return HttpResponse('Authentication was received more than a day ago.')
        except NotTelegramDataError:
            pass #return HttpResponse('The data is not related to Telegram!')
        return telegram_user

class TelegramUser(models.Model):
    persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
    id=models.IntegerField(primary_key=True)
    first_name=models.CharField(max_length=30, blank=True, null=True)
    last_name=models.CharField(max_length=30, blank=True, null=True)
    photo_url=models.CharField(max_length=150, blank=True, null=True)
    auth_date=models.IntegerField(blank=True, null=True)
    hash=models.CharField(max_length=100, blank=True, null=True)


class TelegramUrl(models.Model):
    url=models.CharField(max_length=50, blank=True, null=True)
