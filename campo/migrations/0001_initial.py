# Generated by Django 3.2.3 on 2021-05-28 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clima', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('cant_hectareas', models.IntegerField()),
                ('persona', models.ForeignKey(db_column='persona', null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuario.persona')),
                ('sonda', models.ForeignKey(db_column='sonda', null=True, on_delete=django.db.models.deletion.SET_NULL, to='clima.sonda')),
            ],
        ),
    ]
