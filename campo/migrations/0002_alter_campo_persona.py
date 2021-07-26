# Generated by Django 3.2.3 on 2021-07-26 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_alter_persona_usuario'),
        ('campo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campo',
            name='persona',
            field=models.ForeignKey(db_column='persona', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campo', to='usuario.persona'),
        ),
    ]