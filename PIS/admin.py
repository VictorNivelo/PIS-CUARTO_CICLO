from django.contrib import admin
from .models import (
    UsuarioPersonalizado,
    InformeCarrera,
    InformeMateria,
    InformeCiclo,
    Universidad,
    Facultad,
    Carrera,
    Ciclo,
    Materia
)

admin.site.register(UsuarioPersonalizado)
admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Ciclo)
admin.site.register(Materia)

admin.site.register(InformeCarrera)
admin.site.register(InformeMateria)
admin.site.register(InformeCiclo)
