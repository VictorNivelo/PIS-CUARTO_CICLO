from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsuarioPersonalizado(AbstractUser):
    class Meta:
        pass

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_user_groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_permissions",
    )


# class CustomUser(AbstractUser):

#     class Meta:
#         pass

#     groups = models.ManyToManyField(
#         "auth.Group",
#         verbose_name=_("groups"),
#         blank=True,
#         related_name="custom_user_groups",
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         verbose_name=_("user permissions"),
#         blank=True,
#         related_name="custom_user_permissions",
#     )
