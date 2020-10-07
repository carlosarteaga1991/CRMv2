# Generated by Django 3.0.8 on 2020-10-06 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_auto_20201003_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permisos',
            name='id_usuario',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='apellidos',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=70, unique=True, verbose_name='Correo Electrónico'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombres',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nombres'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=20, unique=True, verbose_name='Usuario'),
        ),
    ]