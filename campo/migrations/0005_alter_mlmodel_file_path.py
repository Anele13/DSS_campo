# Generated by Django 3.2.3 on 2023-03-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campo', '0004_mlmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodel',
            name='file_path',
            field=models.FilePathField(path='/home/anele/Escritorio/tesina/DSS_campo/staticfiles/data'),
        ),
    ]
