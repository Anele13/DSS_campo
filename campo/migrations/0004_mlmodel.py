# Generated by Django 3.2.3 on 2023-03-05 14:06

import django.contrib.staticfiles.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campo', '0003_auto_20221016_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('file_path', models.FilePathField(path=django.contrib.staticfiles.storage.StaticFilesStorage())),
                ('tipo', models.CharField(choices=[('lana', 'lana'), ('corderos', 'corderos'), ('finura', 'finura'), ('rinde', 'rinde')], max_length=10)),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelos_ml', to='campo.campo')),
            ],
        ),
    ]
