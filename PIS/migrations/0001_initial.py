# Generated by Django 5.0.6 on 2024-07-24 21:11

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_carrera', models.CharField(max_length=100, verbose_name='Nombre')),
                ('duracion', models.IntegerField(verbose_name='Duración')),
            ],
        ),
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_facultad', models.CharField(max_length=250, verbose_name='Nombre')),
                ('abreviacion', models.CharField(max_length=100, verbose_name='Abreviación')),
                ('fecha_fundacion', models.DateField(blank=True, null=True, verbose_name='Fecha de Fundación')),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_genero', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion_genero', models.CharField(max_length=100, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_periodo_academico', models.CharField(blank=True, max_length=100, verbose_name='Código')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de Fin')),
                ('estado_periodo_academico', models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], max_length=10, verbose_name='Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_rol', models.CharField(max_length=100, verbose_name='Nombre de Rol')),
                ('descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDNI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo_dni', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion_tipo_dni', models.CharField(max_length=100, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Universidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_universidad', models.CharField(max_length=100, verbose_name='Nombre universidad')),
                ('direccion_universidad', models.CharField(max_length=100, verbose_name='Dirección')),
                ('telefono_universidad', models.CharField(max_length=13, verbose_name='Teléfono')),
                ('correo_universidad', models.EmailField(max_length=100, verbose_name='Correo Electrónico')),
                ('fecha_fundacion', models.DateField(blank=True, null=True, verbose_name='Fecha de Fundación')),
            ],
        ),
        migrations.CreateModel(
            name='Ciclo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ciclo', models.CharField(max_length=100, verbose_name='Nombre')),
                ('numero_ciclo', models.PositiveIntegerField(unique=True, verbose_name='Número')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.carrera', verbose_name='Carrera')),
                ('periodo_academico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.periodoacademico', verbose_name='Período Académico')),
            ],
        ),
        migrations.AddField(
            model_name='carrera',
            name='facultad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.facultad', verbose_name='Facultad'),
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_materia', models.CharField(max_length=100, verbose_name='Nombre')),
                ('numero_horas', models.IntegerField(verbose_name='Número de Horas')),
                ('unidades', models.IntegerField(blank=True, null=True, verbose_name='Unidades')),
                ('ciclo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.ciclo', verbose_name='Ciclo')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni_estudiante', models.CharField(max_length=10, verbose_name='DNI')),
                ('nombre_estudiante', models.CharField(max_length=100, verbose_name='Nombre')),
                ('apellido_estudiante', models.CharField(max_length=100, verbose_name='Apellido')),
                ('modalidad_estudio', models.IntegerField(choices=[(0, 'Presencial'), (1, 'Virtual')], verbose_name='Modalidad de Estudio')),
                ('tipo_educacion', models.IntegerField(choices=[(0, 'Público'), (1, 'Privado')], verbose_name='Tipo de Educación')),
                ('origen', models.IntegerField(choices=[(0, 'No Foráneo'), (1, 'Foráneo')], verbose_name='Origen')),
                ('trabajo', models.IntegerField(choices=[(0, 'No'), (1, 'Sí')], verbose_name='Trabajo')),
                ('discapacidad', models.IntegerField(choices=[(0, 'No'), (1, 'Sí')], verbose_name='Discapacidad')),
                ('hijos', models.IntegerField(choices=[(0, 'No'), (1, 'Sí')], verbose_name='Hijos')),
                ('estado', models.CharField(choices=[('Cursando', 'Cursando'), ('Aprobado', 'Aprobado'), ('Reprovado', 'Reprovado'), ('Desertor', 'Desertor')], max_length=100, verbose_name='Estado')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.genero', verbose_name='Género')),
                ('materia', models.ManyToManyField(to='PIS.materia', verbose_name='Materias')),
                ('tipo_dni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.tipodni', verbose_name='Tipo de DNI')),
            ],
        ),
        migrations.AddField(
            model_name='facultad',
            name='universidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.universidad', verbose_name='Universidad'),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('dni', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='DNI')),
                ('telefono', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono')),
                ('rol', models.CharField(choices=[('Personal Administrativo', 'Personal Administrativo'), ('Secretaria', 'Secretaria'), ('Docente', 'Docente')], max_length=100, verbose_name='Rol')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='Fotos/', verbose_name='Foto')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellido')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superusuario')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.genero', verbose_name='Género')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('tipo_dni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.tipodni', verbose_name='Tipo de DNI')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='materia',
            name='docente_encargado',
            field=models.ForeignKey(limit_choices_to={'rol': 'Docente'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Docente Encargado'),
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo_cuenta', models.EmailField(max_length=100, verbose_name='Correo Electrónico')),
                ('contrasenia_cuenta', models.CharField(max_length=100, verbose_name='Contraseña')),
                ('estado_cuenta', models.BooleanField(verbose_name='Estado de Cuenta')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.rol', verbose_name='Rol')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='DatosHistorico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_matriculados', models.IntegerField(verbose_name='Cantidad de Matriculados')),
                ('cantidad_aprobados', models.IntegerField(verbose_name='Cantidad de Aprobados')),
                ('cantidad_reprobados', models.IntegerField(verbose_name='Cantidad de Reprobados')),
                ('cantidad_desertores', models.IntegerField(verbose_name='Cantidad de Desertores')),
                ('promedio_modalidad', models.FloatField(verbose_name='Promedio Modalidad')),
                ('promedio_tipo_educacion', models.FloatField(verbose_name='Promedio Tipo de Educación')),
                ('promedio_origen', models.FloatField(verbose_name='Promedio Origen')),
                ('promedio_trabajo', models.FloatField(verbose_name='Promedio Trabajo')),
                ('promedio_discapacidad', models.FloatField(verbose_name='Promedio Discapacidad')),
                ('promedio_hijos', models.FloatField(verbose_name='Promedio Hijos')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.materia', verbose_name='Materia')),
                ('periodo_academico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PIS.periodoacademico', verbose_name='Período Académico')),
            ],
            options={
                'unique_together': {('materia', 'periodo_academico')},
            },
        ),
    ]
