# Generated by Django 2.2.3 on 2019-09-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_llave_acceso_ilimitado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispositivo',
            name='numero_serie',
            field=models.CharField(default='', max_length=17),
        ),
    ]