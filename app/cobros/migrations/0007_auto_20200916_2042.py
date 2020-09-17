# Generated by Django 3.0.8 on 2020-09-16 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cobros', '0006_auto_20200915_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='fch_nacimiento',
            field=models.CharField(blank=True, max_length=30, verbose_name='fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cobros.Empresas', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cobros.Usuarios', verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='nombre',
            field=models.CharField(max_length=150, verbose_name='Nombre del cliente'),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='descripcion',
            field=models.CharField(blank=True, max_length=450, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='nombre_contacto',
            field=models.CharField(blank=True, max_length=80, verbose_name='Nombre del contacto'),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='nombre_empresa',
            field=models.CharField(max_length=120, verbose_name='Nombre de la empresa'),
        ),
        migrations.AlterField(
            model_name='empresas',
            name='telefono',
            field=models.CharField(blank=True, max_length=50, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='productos',
            name='capital',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productos',
            name='dias_mora',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productos',
            name='intereses',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productos',
            name='saldo_total',
            field=models.FloatField(),
        ),
    ]
