# Generated by Django 3.2.3 on 2022-10-16 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campo',
            name='latitud',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='campo',
            name='longitud',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
