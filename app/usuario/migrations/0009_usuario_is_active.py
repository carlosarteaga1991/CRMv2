# Generated by Django 3.0.8 on 2020-10-07 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0008_auto_20201006_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]