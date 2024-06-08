from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    
    class Meta:
        pass
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='%(app_label)s_%(class)s_related',
        help_text=_('Specific permissions for this user.')
    )

# class CustomUser(AbstractUser):
#     # Campos adicionales, si los tienes
    
#     class Meta:
#         # Otras configuraciones
#         pass
    
#     # Cambia el related_name en los campos de grupos y permisos
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name=_('groups'),
#         blank=True,
#         related_name='custom_user_groups' # Cambia el related_name aquí
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name=_('user permissions'),
#         blank=True,
#         related_name='custom_user_permissions' # Cambia el related_name aquí
#     )
