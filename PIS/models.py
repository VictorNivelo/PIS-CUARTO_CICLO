from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class UsuarioPersonalizado(AbstractUser):

    ROLES = [
        ("personal_Administrativo", "Personal Administrativo"),
        ("secretaria", "Secretaria"),
        ("docente", "Docente"),
    ]

    rol = models.CharField(max_length=30, choices=ROLES, default="docente")
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
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
