# Generated by Django 2.2.3 on 2019-08-05 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0009_auto_20190731_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispositivo',
            name='numero_serie',
            field=models.CharField(default='', max_length=20),
        ),
    ]