# Generated by Django 3.0.8 on 2020-09-18 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobros', '0011_remove_gestiones_fch_creacion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gestiones',
            options={'ordering': ['-fch_gestion'], 'verbose_name_plural': 'Gestiones'},
        ),
    ]