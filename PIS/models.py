from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UsuarioPersonalizado(AbstractUser):

    USERNAME_FIELD = "NombreUsuario"
    REQUIRED_FIELDS = ["Correo"]

    NombreUsuario = models.CharField(max_length=50, unique=True)
    Correo = models.EmailField(max_length=254, unique=True)
    Contrasenia = models.CharField(max_length=50)
    Confirmar_Contrasenia = models.CharField(max_length=50)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        verbose_name=_("groups"),
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_set",
    )

    def __str__(self):
        return self.NombreUsuario
