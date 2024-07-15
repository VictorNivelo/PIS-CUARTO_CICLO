from django.contrib import admin
from .models import (
    DatosHistoricos,
    Estudiante,
    PeriodoAcademico,
    UsuarioPersonalizado,
    InformeCarrera,
    InformeMateria,
    InformeCiclo,
    Universidad,
    Facultad,
    Carrera,
    Ciclo,
    Materia,
    Genero,
    TipoDNI,
)

admin.site.register(UsuarioPersonalizado)
admin.site.register(Estudiante)
admin.site.register(Genero)
admin.site.register(TipoDNI)
admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Ciclo)
admin.site.register(Materia)
admin.site.register(PeriodoAcademico)
admin.site.register(DatosHistoricos)

admin.site.register(InformeCarrera)
admin.site.register(InformeMateria)
admin.site.register(InformeCiclo)
