from django.contrib import admin
from .models import (
    PeriodoAcademico,
    DatosHistorico,
    Universidad,
    Estudiante,
    Facultad,
    Usuario,
    TipoDNI,
    Carrera,
    Materia,
    Genero,
    Ciclo,
)

admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Genero)
admin.site.register(TipoDNI)
admin.site.register(Universidad)
admin.site.register(Facultad)
admin.site.register(Carrera)
admin.site.register(Ciclo)
admin.site.register(Materia)
admin.site.register(PeriodoAcademico)
admin.site.register(DatosHistorico)

# admin.site.register(InformeCarrera)
# admin.site.register(InformeMateria)
# admin.site.register(InformeCiclo)
