# Generated by Django 2.2.3 on 2019-07-31 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0008_llave_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llave',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]