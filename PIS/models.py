from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class UsuarioPersonalizado(AbstractUser):

    ROLES = [
        ("personal_Administrativo", "Personal Administrativo"),
        ("secretaria", "Secretaria"),
        ("docente", "Docente"),
    ]

    GENERO_OPCIONES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
        ("O", "Otro"),
    ]

    TIPO_DNI_OPCIONES = [
        ("Pasaporte", "Pasaporte"),
        ("Cedula", "Cédula de Identidad"),
    ]

    genero = models.CharField(
        max_length=1,
        choices=GENERO_OPCIONES,
        blank=True,
        null=True,
        verbose_name="Género",
    )
    fecha_nacimiento = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Nacimiento"
    )
    dni = models.CharField(max_length=10, blank=True, null=True, verbose_name="DNI")
    tipo_dni = models.CharField(
        max_length=20,
        choices=TIPO_DNI_OPCIONES,
        blank=True,
        null=True,
        verbose_name="Tipo de DNI",
    )
    telefono = models.CharField(
        max_length=10, blank=True, null=True, verbose_name="Teléfono"
    )
    rol = models.CharField(max_length=50, choices=ROLES, default="docente")
    # rol = models.CharField(max_length=30, choices=ROLES, blank=True, null=True, verbose_name="Rol")
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
        self.email = self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"


class InformeCarrera(models.Model):
    carrera = models.CharField(max_length=100, verbose_name="Carrera")
    numero_estudiantes = models.IntegerField(verbose_name="Número de Estudiantes")
    aprobados = models.IntegerField(verbose_name="Aprobados")
    reprobados = models.IntegerField(verbose_name="Reprobados")
    desertores = models.IntegerField(verbose_name="Desertores")
    retirados = models.IntegerField(verbose_name="Retirados")

    class Meta:
        verbose_name = "Informe de Carrera"
        verbose_name_plural = "Informes de Carreras"

    def __str__(self):
        return self.carrera


class InformeCiclo(models.Model):
    ciclo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    numero_estudiantes = models.IntegerField()
    aprobados = models.IntegerField()
    reprobados = models.IntegerField()
    desertores = models.IntegerField()
    retirados = models.IntegerField()

    def __str__(self):
        return self.ciclo


class InformeMateria(models.Model):
    materia = models.CharField(max_length=100)
    docente_encargado = models.CharField(max_length=100)
    num_estudiantes = models.IntegerField()
    aprobados = models.IntegerField()
    reprobados = models.IntegerField()
    desertores = models.IntegerField()
    retirados = models.IntegerField()

    def __str__(self):
        return self.materia


class Universidad(models.Model):
    nombre_universidad = models.CharField(max_length=100, verbose_name="Nombre")
    direccion = models.CharField(max_length=100, verbose_name="Dirección")
    telefono = models.CharField(max_length=10, verbose_name="Teléfono")
    correo = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    fecha_fundacion = models.DateField(verbose_name="Fecha de Fundación")

    def __str__(self):
        return self.nombre_universidad


class Facultad(models.Model):
    nombre_facultad = models.CharField(max_length=100, verbose_name="Nombre")
    fecha_fundacion = models.DateField(verbose_name="Fecha de Fundación")
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
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    carrera = models.ForeignKey(
        Carrera, on_delete=models.CASCADE, verbose_name="Carrera"
    )

    def __str__(self):
        return self.nombre_ciclo


class Materia(models.Model):
    nombre_materia = models.CharField(max_length=100, verbose_name="Nombre")
    numero_horas = models.IntegerField(verbose_name="Número de Horas")
    docente_encargado = models.CharField(
        max_length=100, verbose_name="Docente Encargado"
    )
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, verbose_name="Ciclo")

    def __str__(self):
        return self.nombre_materia


class Informe(models.Model):
    fecha_creacion = models.DateField(verbose_name="Fecha de Creación")

    def __str__(self):
        return self.usuario.username


# Poco usadas


class Factor(models.Model):
    nombre_factor = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")

    def __str__(self):
        return self.nombre_factor


class Usuario(models.Model):
    tipo_dni = models.CharField(max_length=20, verbose_name="Tipo de DNI")
    numero_dni = models.CharField(max_length=10, verbose_name="Número de DNI")
    nombre_usuario = models.CharField(max_length=100, verbose_name="Nombre de Usuario")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    telefono = models.CharField(max_length=10, verbose_name="Teléfono")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    genero = models.CharField(max_length=1, verbose_name="Género")

    def __str__(self):
        return self.nombre_usuario


class Cuenta(models.Model):
    correo_cuenta = models.EmailField(max_length=100, verbose_name="Correo Electrónico")
    contrasenia_cuenta = models.CharField(max_length=100, verbose_name="Contraseña")
    estado_cuenta = models.BooleanField(verbose_name="Estado de Cuenta")
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )

    def __str__(self):
        return self.correo_cuenta


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, verbose_name="Nombre de Rol")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )

    def __str__(self):
        return self.nombre_rol


class PersonalAdministrativo(models.Model):
    codigo_personal_administrativo = models.CharField(
        max_length=100, verbose_name="Código"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )

    def __str__(self):
        return self.codigo_personal_administrativo


class Secretaria(models.Model):
    codigo_secretaria = models.CharField(max_length=100, verbose_name="Código")
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )

    def __str__(self):
        return self.codigo_secretaria


class Docente(models.Model):
    codigo_docente = models.CharField(max_length=100, verbose_name="Código")
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, verbose_name="Usuario"
    )

    def __str__(self):
        return self.codigo_docente
