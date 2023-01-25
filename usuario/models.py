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
            if result:
                if not TelegramUser.objects.filter(id=result['id']).exists():
                    user_data = result.dict()
                    user_data.update({'persona':self})
                    telegram_user = TelegramUser.objects.create(**user_data)
                else: 
                    telegram_user = TelegramUser.objects.get(id=result['id'])
                    telegram_user.refresh_firebase_data()
        except TelegramDataIsOutdatedError:
            pass #return HttpResponse('Authentication was received more than a day ago.')
        except NotTelegramDataError:
            pass #return HttpResponse('The data is not related to Telegram!')
        return telegram_user

class TelegramUser(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    id=models.IntegerField(primary_key=True)
    first_name=models.CharField(max_length=30, blank=True, null=True)
    last_name=models.CharField(max_length=30, blank=True, null=True)
    photo_url=models.CharField(max_length=150, blank=True, null=True)
    auth_date=models.IntegerField(blank=True, null=True)
    hash=models.CharField(max_length=100, blank=True, null=True)

    def refresh_firebase_data(self):
        from firebase_admin import db
        data = {
            'auth_date': self.auth_date, 
            'campo_id': self.persona.campo.first().id,
            'first_name': self.first_name, 
            'last_name': self.last_name,
            'photo_url': self.photo_url,
        }
        db.reference(f'user/{self.id}/').set(data)


class TelegramUrl(models.Model):
    url=models.CharField(max_length=50, blank=True, null=True)
