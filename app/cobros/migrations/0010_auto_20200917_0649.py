# Generated by Django 3.0.8 on 2020-09-17 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobros', '0009_auto_20200917_0609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='motivos',
            old_name='descripción',
            new_name='descripcion',
        ),
    ]
