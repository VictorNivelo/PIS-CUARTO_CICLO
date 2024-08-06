# Generated by Django 5.0.6 on 2024-08-04 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PIS', '0002_alter_ciclo_numero_ciclo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoshistorico',
            name='cantidad_aprobados',
            field=models.PositiveIntegerField(verbose_name='Cantidad de Aprobados'),
        ),
        migrations.AlterField(
            model_name='datoshistorico',
            name='cantidad_desertores',
            field=models.PositiveIntegerField(verbose_name='Cantidad de Desertores'),
        ),
        migrations.AlterField(
            model_name='datoshistorico',
            name='cantidad_matriculados',
            field=models.PositiveIntegerField(verbose_name='Cantidad de Matriculados'),
        ),
        migrations.AlterField(
            model_name='datoshistorico',
            name='cantidad_reprobados',
            field=models.PositiveIntegerField(verbose_name='Cantidad de Reprobados'),
        ),
    ]
