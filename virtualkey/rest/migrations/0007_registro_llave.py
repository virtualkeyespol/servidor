# Generated by Django 2.2.3 on 2019-07-24 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0006_auto_20190724_0559'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='llave',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='rest.Llave'),
        ),
    ]