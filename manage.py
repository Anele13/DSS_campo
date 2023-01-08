#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Timer
import tempfile
from django.conf import settings

fo = tempfile.NamedTemporaryFile()

def read_production_url():
    url = fo.read().decode('latin-1')
    c = url.split(' ')[-1:][0].replace('/n','')
    os.environ['TELEGRAM_LOGIN_REDIRECT_URL'] = f'/perfil'
    print(f'External url: {c}')
    from usuario.models import TelegramUrl
    if TelegramUrl.objects.all().count() == 0:
        t = TelegramUrl()
        t.url = f'{c}/perfil' 
        t.save()
    else:
        t = TelegramUrl.objects.first()
        t.url = f'{c}/perfil'  
        t.save()
    try:
        fo.close()
    except:
        pass

def run_lt(port):
    cmd = f'lt --p {port} > {fo.name}'
    c =  os.system(cmd)

def run_with_lt(port):
    thread = Timer(1, run_lt, args=(port,))
    thread.setDaemon(True)
    thread.start()

    thread = Timer(3, read_production_url)
    thread.setDaemon(True)
    thread.start()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_campo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if os.environ.get('RUN_MAIN', False) and settings.ENVIRONMENT != 'Local':
        run_with_lt(8000)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
