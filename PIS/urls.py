from django.contrib import admin
from django.urls import path
from .vistas import (
    GestionTipoDNI,
    PaginaPrincipal,
    
    IniciarSesion,
    CerrarSesion,
    RegistrarUsuario,
    RecuperarContrasenia,
    
    InformeMateria,
    InformeCiclo,
    InformeCarrera,
    
    Informacion1,
    Informacion2,
    Informacion3,
    Informacion4,
    
    Grafico,
    Galeria,
    Prediccion,
    PrediccionPresente,
    Reporte,
    CargarInforme,
    
    PaginaAdministrador,
    PaginaDocente,
    PaginaSecretaria,
    
    RegistrarUniversidad,
    RegistrarTipoDNI,
    RegistrarGenero,
    RegistrarFacultad,
    RegistrarCarrera,
    RegistrarCarrera,
    RegistrarCiclo,
    RegistrarMateria,
    
    GestionUsuario,
    GestionGenero,
    GestionUniversidad,
    GestionFacultad,
    GestionCarrera,
    GestionCiclo,
    GestionMateria,
    upload_universities,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", PaginaPrincipal, name="Index"),
    path("Pagina-Administrador/", PaginaAdministrador, name="Pagina_Administrador"),
    path("Pagina-Secretaria/", PaginaSecretaria, name="Pagina_Secretaria"),
    path("Pagina-Docente/", PaginaDocente, name="Pagina_Docente"),
    
    path("Registrar-Usuario/", RegistrarUsuario, name="Registrar_Usuario"),
    path("Registrar-TipoDNI/", RegistrarTipoDNI, name="Registrar_TipoDNI"),
    path("Registrar-Genero/", RegistrarGenero, name="Registrar_Genero"),
    path("Registrar-Universidad/", RegistrarUniversidad, name="Registrar_Universidad"),
    path("Registrar-Facultad/", RegistrarFacultad, name="Registrar_Facultad"),
    path("Registrar-Carrera/", RegistrarCarrera, name="Registrar_Carrera"),
    path("Registrar-Ciclo/", RegistrarCiclo, name="Registrar_Ciclo"),
    path("Registrar-Materia/", RegistrarMateria, name="Registrar_Materia"),
    
    path("Iniciar-Sesion/", IniciarSesion, name="Iniciar_Sesion"),
    path("Cerrar-Sesion/", CerrarSesion, name="Cerrar_Sesion"),
    path("Recuperar-Contrasenia/", RecuperarContrasenia, name="Recuperar_Contrasenia"),
    
    path("Informe-Materia/", InformeMateria, name="Informe_Materia"),
    path("Informe-Ciclo/", InformeCiclo, name="Informe_Ciclo"),
    path("Informe-Carrera/", InformeCarrera, name="Informe_Carrera"),
    
    path("Informacion-1/", Informacion1, name="Informacion_1"),
    path("Informacion-2/", Informacion2, name="Informacion_2"),
    path("Informacion-3/", Informacion3, name="Informacion_3"),
    path("Informacion-4/", Informacion4, name="Informacion_4"),

    path("Grafico/", Grafico, name="Grafico"),
    path("Galeria/", Galeria, name="Galeria"),
    path("Prediccion/", Prediccion, name="Prediccion"),
    path("PrediccionP/", PrediccionPresente, name="Prediccion_Presente"),
    path("Reporte-Generado/", Reporte, name="Reporte_Generado"),
    path("Cargar-Informe/", CargarInforme, name="Cargar_Informe"),
    
    path("Gestion-Universidad/", GestionUniversidad, name="Gestion_Universidad"),
    path("Gestion-TipoDNI/", GestionTipoDNI, name="Gestion_TipoDNI"),
    path("Gestion-Genero/", GestionGenero, name="Gestion_Genero"),
    path("Gestion-Usuarios/", GestionUsuario, name="Gestion_Usuario"),
    path("Gestion-Facultad/", GestionFacultad, name="Gestion_Facultad"),
    path("Gestion-Carrera/", GestionCarrera, name="Gestion_Carrera"),
    path("Gestion-Ciclo/", GestionCiclo, name="Gestion_Ciclo"),
    path("Gestion-Materia/", GestionMateria, name="Gestion_Materia"),

    path('upload-universities/', upload_universities, name='upload_universities'),
]
