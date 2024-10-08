from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = [
        ("Personal Administrativo", "Personal Administrativo"),
        ("Secretaria", "Secretaria"),
        ("Docente", "Docente"),
    ]
    genero = models.ForeignKey(
        "Genero", on_delete=models.CASCADE, verbose_name="Género"
    )
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    dni = models.CharField(
        max_length=10, unique=True, db_index=True, verbose_name="DNI"
    )
    tipo_dni = models.ForeignKey(
        "TipoDNI", on_delete=models.CASCADE, verbose_name="Tipo de DNI"
    )
    telefono = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Teléfono"
    )
    rol = models.CharField(max_length=100, choices=ROLES, verbose_name="Rol")
    foto = models.ImageField(
        upload_to="Fotos/", null=True, blank=True, verbose_name="Foto"
    )
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    is_superuser = models.BooleanField(default=False, verbose_name="Superusuario")
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "dni",
    ]

    def save(self, *args, **kwargs):
        self.full_clean()
        self.email = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {"  -  "} {self.dni}"


class Genero(models.Model):
    nombre_genero = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion_genero = models.CharField(max_length=100, verbose_name="Descripción")

    def __str__(self):
        return self.nombre_genero


class TipoDNI(models.Model):
    nombre_tipo_dni = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion_tipo_dni = models.CharField(max_length=100, verbose_name="Descripción")

    def __str__(self):
        return self.nombre_tipo_dni


class Universidad(models.Model):
    nombre_universidad = models.CharField(
        max_length=100, verbose_name="Nombre universidad"
    )
    direccion_universidad = models.CharField(max_length=100, verbose_name="Dirección")
    telefono_universidad = models.CharField(max_length=13, verbose_name="Teléfono")
    correo_universidad = models.EmailField(
        max_length=100, verbose_name="Correo Electrónico"
    )
    fecha_fundacion = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Fundación"
    )

    def __str__(self):
        return self.nombre_universidad


class Facultad(models.Model):
    nombre_facultad = models.CharField(max_length=250, verbose_name="Nombre")
    abreviacion = models.CharField(max_length=100, verbose_name="Abreviación")
    fecha_fundacion = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Fundación"
    )
    universidad = models.ForeignKey(
        Universidad, on_delete=models.CASCADE, verbose_name="Universidad"
    )

    def __str__(self):
        return self.nombre_facultad


class Carrera(models.Model):
    nombre_carrera = models.CharField(max_length=100, verbose_name="Nombre")
    duracion = models.IntegerField(verbose_name="Duración")
    facultad = models.ForeignKey(
        Facultad, on_delete=models.CASCADE, verbose_name="Facultad"
    )

    def __str__(self):
        return self.nombre_carrera


class Ciclo(models.Model):
    nombre_ciclo = models.CharField(max_length=100, verbose_name="Nombre")
    numero_ciclo = models.PositiveIntegerField(verbose_name="Número")
    carrera = models.ForeignKey(
        Carrera, on_delete=models.CASCADE, verbose_name="Carrera"
    )
    periodo_academico = models.ForeignKey(
        "PeriodoAcademico", on_delete=models.CASCADE, verbose_name="Período Académico"
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.numero_ciclo = Ciclo.objects.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_ciclo


class Materia(models.Model):
    nombre_materia = models.CharField(max_length=100, verbose_name="Nombre")
    numero_horas = models.IntegerField(verbose_name="Número de Horas")
    unidades = models.IntegerField(null=True, blank=True, verbose_name="Unidades")
    docente_encargado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        verbose_name="Docente Encargado",
        limit_choices_to={"rol": "Docente"},
    )
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, verbose_name="Ciclo")

    def __str__(self):
        return self.nombre_materia


class PeriodoAcademico(models.Model):
    codigo_periodo_academico = models.CharField(
        max_length=100, verbose_name="Código", blank=True
    )
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    estado_periodo_academico = models.CharField(
        max_length=10,
        choices=[("Activo", "Activo"), ("Inactivo", "Inactivo")],
        verbose_name="Estado",
    )

    def save(self, *args, **kwargs):
        if not self.codigo_periodo_academico:
            meses = [
                "Enero",
                "Febrero",
                "Marzo",
                "Abril",
                "Mayo",
                "Junio",
                "Julio",
                "Agosto",
                "Septiembre",
                "Octubre",
                "Noviembre",
                "Diciembre",
            ]
            mes_inicio = meses[self.fecha_inicio.month - 1]
            mes_fin = meses[self.fecha_fin.month - 1]
            self.codigo_periodo_academico = f"{mes_inicio}-{self.fecha_inicio.year} - {mes_fin}-{self.fecha_fin.year}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo_periodo_academico


class DatosHistorico(models.Model):
    materia = models.ForeignKey(
        Materia, on_delete=models.CASCADE, verbose_name="Materia"
    )
    periodo_academico = models.ForeignKey(
        "PeriodoAcademico", on_delete=models.CASCADE, verbose_name="Período Académico"
    )
    cantidad_matriculados = models.PositiveIntegerField(verbose_name="Cantidad de Matriculados")
    cantidad_aprobados = models.PositiveIntegerField(verbose_name="Cantidad de Aprobados")
    cantidad_reprobados = models.PositiveIntegerField(verbose_name="Cantidad de Reprobados")
    cantidad_desertores = models.PositiveIntegerField(verbose_name="Cantidad de Desertores")
    promedio_modalidad = models.FloatField(verbose_name="Promedio Modalidad")
    promedio_tipo_educacion = models.FloatField(
        verbose_name="Promedio Tipo de Educación"
    )
    promedio_origen = models.FloatField(verbose_name="Promedio Origen")
    promedio_trabajo = models.FloatField(verbose_name="Promedio Trabajo")
    promedio_discapacidad = models.FloatField(verbose_name="Promedio Discapacidad")
    promedio_hijos = models.FloatField(verbose_name="Promedio Hijos")

    class Meta:
        unique_together = ("materia", "periodo_academico")

    def __str__(self):
        return f"{self.materia} - {self.periodo_academico}"


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100, verbose_name="Nombre de Rol")
    descripcion = models.CharField(max_length=100, verbose_name="Descripción")

    def __str__(self):
        return self.nombre_rol


class Cuenta(models.Model):
    correo_cuenta = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    contrasenia_cuenta = models.CharField(max_length=100, verbose_name="Contraseña")
    estado_cuenta = models.BooleanField(verbose_name="Estado de Cuenta")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, verbose_name="Rol")
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )

    def __str__(self):
        return self.correo_cuenta


class Estudiante(models.Model):
    tipo_dni = models.ForeignKey(
        "TipoDNI", on_delete=models.CASCADE, verbose_name="Tipo de DNI"
    )
    dni_estudiante = models.CharField(max_length=10, verbose_name="DNI")
    nombre_estudiante = models.CharField(max_length=100, verbose_name="Nombre")
    apellido_estudiante = models.CharField(max_length=100, verbose_name="Apellido")
    genero = models.ForeignKey(
        "Genero",
        on_delete=models.CASCADE,
        verbose_name="Género",
    )
    MODALIDAD_ESTUDIO_CHOICES = (
        (0, "Presencial"),
        (1, "Virtual"),
    )
    modalidad_estudio = models.IntegerField(
        choices=MODALIDAD_ESTUDIO_CHOICES, verbose_name="Modalidad de Estudio"
    )
    TIPO_EDUCACION_CHOICES = (
        (0, "Público"),
        (1, "Privado"),
    )
    tipo_educacion = models.IntegerField(
        choices=TIPO_EDUCACION_CHOICES, verbose_name="Tipo de Educación"
    )
    ORIGEN_CHOICES = (
        (0, "No Foráneo"),
        (1, "Foráneo"),
    )
    origen = models.IntegerField(choices=ORIGEN_CHOICES, verbose_name="Origen")
    TRABAJA_CHOICES = (
        (0, "No"),
        (1, "Sí"),
    )
    trabajo = models.IntegerField(choices=TRABAJA_CHOICES, verbose_name="Trabajo")
    DISCAPACIDAD_CHOICES = (
        (0, "No"),
        (1, "Sí"),
    )
    discapacidad = models.IntegerField(
        choices=DISCAPACIDAD_CHOICES, verbose_name="Discapacidad"
    )
    HIJOS_CHOICES = (
        (0, "No"),
        (1, "Sí"),
    )
    hijos = models.IntegerField(choices=HIJOS_CHOICES, verbose_name="Hijos")
    ESTADO_CHOICES = (
        ("Cursando", "Cursando"),
        ("Aprobado", "Aprobado"),
        ("Reprovado", "Reprovado"),
        ("Desertor", "Desertor"),
    )
    estado = models.CharField(
        choices=ESTADO_CHOICES, max_length=100, verbose_name="Estado"
    )
    materia = models.ManyToManyField("Materia", verbose_name="Materias")

    def __str__(self):
        return (
            f"{self.nombre_estudiante} {self.apellido_estudiante} {self.dni_estudiante}"
        )
