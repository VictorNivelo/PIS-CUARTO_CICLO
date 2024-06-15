from django.contrib import admin
from .models import UsuarioPersonalizado, InformeCarrera, InformeMateria, InformeCiclo

admin.site.register(UsuarioPersonalizado)
admin.site.register(InformeCarrera)
admin.site.register(InformeMateria)
admin.site.register(InformeCiclo)
