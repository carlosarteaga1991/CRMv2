# Generated by Django 3.0.8 on 2020-09-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobros', '0013_auto_20200924_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordatorios',
            name='hora_recordatorio',
            field=models.TimeField(default='00:00:00'),
        ),
    ]
