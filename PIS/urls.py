from django.contrib import admin
from django.urls import path
from .Vistas import (
    Hola, PaginaPrincipal, Pagina_Administrador, iniciar_sesion, registrar_usuario, Recuperar,
    InformeMateria, InformeCiclo, InformeCarrera,
    Informacion1, Informacion2, Informacion3, Informacion4,
    Grafico, Galeria, Prediccion, PrediccionPresente, Reporte,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Hola/", Hola, name="Hola"),
    path("", PaginaPrincipal, name="Index"),
    path("Pagina-Administrador/", Pagina_Administrador, name="Pagina_administrador"),
    path("Iniciar-Sesion/", iniciar_sesion, name="Iniciar_sesion"),
    path("Recuperar-Contrasenia/", Recuperar, name="RecuperarContrasenia"),
    path("Registrar-Usuario/", registrar_usuario, name="Registrar_usuario"),
    # path("signin/", signin, name="signin"),
    # path("signup/", signup, name="signup"),
    path("Informe-Materia/", InformeMateria, name="InformeMateria"),
    path("Informe-Ciclo/", InformeCiclo, name="InformeCiclo"),
    path("Informe-Carrera/", InformeCarrera, name="InformeCarrera"),
    path("Informacion-1/", Informacion1, name="Informacion1"),
    path("Informacion-2/", Informacion2, name="Informacion2"),
    path("Informacion-3/", Informacion3, name="Informacion3"),
    path("Informacion-4/", Informacion4, name="Informacion4"),
    path("Grafico/", Grafico, name="Grafico"),
    path("Galeria/", Galeria, name="Galeria"),
    path("Prediccion/", Prediccion, name="Prediccion"),
    path("PP/", PrediccionPresente, name="PrediccionPresente"),
    path("Reporte-Generado/", Reporte, name="ReporteGenerado"),
]