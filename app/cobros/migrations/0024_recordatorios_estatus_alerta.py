# Generated by Django 3.0.8 on 2020-10-01 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobros', '0023_auto_20200930_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordatorios',
            name='estatus_alerta',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Atendida', 'Atendida')], default='Pendiente', max_length=11, verbose_name='Estatus de la Alerta'),
        ),
    ]
