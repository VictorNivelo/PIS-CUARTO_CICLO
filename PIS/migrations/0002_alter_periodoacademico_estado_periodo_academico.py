# Generated by Django 5.0.6 on 2024-07-04 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PIS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodoacademico',
            name='estado_periodo_academico',
            field=models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=10, verbose_name='Estado'),
        ),
    ]
