from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path
from .vistas import (
    PaginaPrincipal,
    PaginaAyuda,
    PaginaAdministrador,
    PaginaDocente,
    PaginaSecretaria,
    
    IniciarSesion,
    CerrarSesion,
    RecuperarContrasenia,
    CambiarContrasenia,
    CorreoEnviado,
    PerfilUsuario,
    EliminarFotoPerfil,
    
    RegistrarUniversidad,
    RegistrarTipoDNI,
    RegistrarGenero,
    RegistrarUsuario,
    RegistrarEstudiante,
    RegistrarFacultad,
    RegistrarCarrera,
    RegistrarCarrera,
    RegistrarCiclo,
    RegistrarMateria,
    RegistrarPeriodoAcademico,
    RegistrarDatosHistorico,
    
    GestionUniversidad,
    GestionGenero,
    GestionTipoDNI,
    GestionUsuario,
    GestionFacultad,
    GestionCarrera,
    GestionCiclo,
    GestionMateria,
    GestionEstudiante,
    GestionDatosHistoricos,
    GestionPeriodoAcademico,
    
    ImportarDatosModelo,
    ImportarUsuario,
    ImportarEstudiante,
    ImportarUniversidades,
    ImportarFacultades,
    ImportarCarreras,
    ImportarCiclos,
    ImportarMaterias,
    ImportarPeriodoAcademicos,
    ImportarGenero,
    ImportarTipoDNI,
    ImportarDatoHistoricos,
    
    ObtenerUniversidades,
    ObtenerFacultades,
    ObtenerCarreras,
    ObtenerCiclos,
    ObtenerMaterias,
    ObtenerDocentes,

    PrediccionMateria,
    PrediccionCiclo,
    PrediccionCarrera,
    RealizarPrediccion,
    RealizarPrediccionCiclo,
    RealizarPrediccionCarrera,

    PRI,
    SinAcceso,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", PaginaPrincipal, name="Index"),
    path("Pagina-Ayuda", PaginaAyuda, name="Pagina_Ayuda"),
    path("Pagina-Administrador/", PaginaAdministrador, name="Pagina_Administrador"),
    path("Pagina-Secretaria/", PaginaSecretaria, name="Pagina_Secretaria"),
    path("Pagina-Docente/", PaginaDocente, name="Pagina_Docente"),
    
    path("Registrar-Usuario/", RegistrarUsuario, name="Registrar_Usuario"),
    path("Registrar-Estudiante/", RegistrarEstudiante, name="Registrar_Estudiante"),
    path("Registrar-TipoDNI/", RegistrarTipoDNI, name="Registrar_TipoDNI"),
    path("Registrar-Genero/", RegistrarGenero, name="Registrar_Genero"),
    path("Registrar-Universidad/", RegistrarUniversidad, name="Registrar_Universidad"),
    path("Registrar-Facultad/", RegistrarFacultad, name="Registrar_Facultad"),
    path("Registrar-Carrera/", RegistrarCarrera, name="Registrar_Carrera"),
    path("Registrar-Ciclo/", RegistrarCiclo, name="Registrar_Ciclo"),
    path("Registrar-PeriodoAcademico/", RegistrarPeriodoAcademico, name="Registrar_PeriodoAcademico"),
    path("Registrar-Materia/", RegistrarMateria, name="Registrar_Materia"),
    path("Registrar-DatosHistorico/", RegistrarDatosHistorico, name="Registrar_DatosHistorico"),

    path("Gestion-Estudiante/", GestionEstudiante, name="Gestion_Estudiante"),
    path("Gestion-Usuarios/", GestionUsuario, name="Gestion_Usuario"),
    path("Gestion-TipoDNI/", GestionTipoDNI, name="Gestion_TipoDNI"),
    path("Gestion-Genero/", GestionGenero, name="Gestion_Genero"),
    path("Gestion-Universidad/", GestionUniversidad, name="Gestion_Universidad"),
    path("Gestion-Facultad/", GestionFacultad, name="Gestion_Facultad"),
    path("Gestion-Carrera/", GestionCarrera, name="Gestion_Carrera"),
    path("Gestion-PeriodoAcademico/", GestionPeriodoAcademico, name="Gestion_PeriodoAcademico"),
    path("Gestion-Ciclo/", GestionCiclo, name="Gestion_Ciclo"),
    path("Gestion-Materia/", GestionMateria, name="Gestion_Materia"),
    path("Gestion-DatosHistorico/", GestionDatosHistoricos, name="Gestion_DatosHistorico"),

    path('Importar-Datos/', ImportarDatosModelo, name='Importar_Datos'),

    path('Importar-Usuario/',ImportarUsuario, name='Importar_Usuario'),
    path('Importar-Estudiante/',ImportarEstudiante, name='Importar_Estudiante'),
    path('Importar-Genero/',ImportarGenero, name='Importar_Genero'),
    path('Importar-TipoDNI/',ImportarTipoDNI, name='Importar_TipoDNI'),
    path('Importar-Universidades/',ImportarUniversidades, name='Importar_Universidades'),
    path('Importar-Facultades/',ImportarFacultades, name='Importar_Facultades'),
    path('Importar-Carreras/',ImportarCarreras, name='Importar_Carreras'),
    path("Importar-Ciclos/",ImportarCiclos, name="Importar_Ciclos"),
    path("Importar-Materias/",ImportarMaterias, name="Importar_Materias"),
    path("Importar-PeriodoAcademicos/",ImportarPeriodoAcademicos, name="Importar_PeriodoAcademicos"),
    path("Importar-DatosHistoricos/",ImportarDatoHistoricos, name="Importar_DatosHistoricos"),
    
    path("Iniciar-Sesion/", IniciarSesion, name="Iniciar_Sesion"),
    path("Cerrar-Sesion/", CerrarSesion, name="Cerrar_Sesion"),
    path("Recuperar-Contrasenia/", RecuperarContrasenia, name="Recuperar_Contrasenia"),
    path("Cambiar-Contrasenia/<uidb64>/<token>/", CambiarContrasenia, name="Cambiar_Contrasenia"),
    path('Correo-Enviado/<uidb64>/<token>/', CorreoEnviado, name='Correo_Enviado'),
    path('Perfil-Usuario/', PerfilUsuario, name='Perfil_Usuario'),
    path('Eliminar-Foto/', EliminarFotoPerfil, name='Eliminar_Foto'),

    path('Obtener-Universidad/', ObtenerUniversidades, name='Obtener_Universidad'),
    path('Obtener-Facultad', ObtenerFacultades, name='Obtener_Facultades'),
    path('Obtener-Carrera/', ObtenerCarreras, name='Obtener_Carreras'),
    path('Obtener-Ciclo/', ObtenerCiclos, name='Obtener_Ciclos'),
    path('Obtener-materia/', ObtenerMaterias, name='Obtener_Materias'),
    path('Obtener-Docente/', ObtenerDocentes, name='Obtener_Docentes'),

    path('Prediccion-Carrera/',PrediccionCarrera, name='Prediccion_Carrera'),
    path('Realizar-Prediccion-Carrera/',RealizarPrediccionCarrera, name='Realizar_Prediccion_Carrera'),
    path('Prediccion-Materia/', PrediccionMateria, name='Prediccion_Materia'),
    path('Prediccion-Ciclo/', PrediccionCiclo, name='Prediccion_Ciclo'),
    path('Realizar-Prediccion/',RealizarPrediccion, name='Realizar_Prediccion'),
    path('Realizar-Prediccion-Ciclo/',RealizarPrediccionCiclo, name='Realizar_Prediccion_Ciclo'),
    
    # path('Prediccion-Desercion/', Predecir_Desercion, name='Predecir_Desercion'),

    # path('Predecir/', PredecirDesercion, name='Predecir_Desercion'),
    path('1/',PRI, name='PI'),
    path('Sin-Acceso/',SinAcceso, name='Sin_Acceso'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
