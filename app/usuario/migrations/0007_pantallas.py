# Generated by Django 3.0.8 on 2020-10-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0006_auto_20201006_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pantallas',
            fields=[
                ('id_pantalla', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Pantalla')),
            ],
            options={
                'verbose_name_plural': 'Pantallas',
                'ordering': ['id_pantalla'],
            },
        ),
    ]
