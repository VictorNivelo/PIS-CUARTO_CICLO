# Generated by Django 5.0.6 on 2024-07-12 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PIS', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Datos_Historicos',
            new_name='DatosHistoricos',
        ),
        migrations.AlterModelOptions(
            name='datoshistoricos',
            options={},
        ),
    ]
