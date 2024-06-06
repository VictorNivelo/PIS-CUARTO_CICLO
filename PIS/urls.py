from django.contrib import admin
from django.urls import path
from .Vistas import PaginaPrincipal, signin, signup, Prediccion, Recuperar, Reporte ,InformeMateria, InformeCarrera, InformeCiclo, Hola, p, gallery, full_width, sidebar_left, sidebar_right, basic_grid, Grafico, iniciar_sesion, Pagina_Administrador, registrar_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Pagina-Principal', PaginaPrincipal, name='PaginaPrincipal'),
    path('Hola/', Hola, name='Hola'),
    path('', p, name='index'),
    path('Galeria/', gallery, name='gallery'),
    path('Informacion-1/', full_width, name='full_width'),
    path('Informacion-2/', sidebar_left, name='sidebar_left'),
    path('Informacion-3/', sidebar_right, name='sidebar_right'),
    path('Informacion-4/', basic_grid, name='basic_grid'),
    path('Grafico/', Grafico, name='grafico'),
    path('Iniciar-Sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('Pagina-Administrador/', Pagina_Administrador, name='pagina_administrador'),
    path('Registrar-Usuario/', registrar_usuario, name='registrar_usuario'),
    path('Informe-Materia/', InformeMateria, name='InformeMateria'),
    path('Informe-Ciclo/', InformeCiclo, name='InformeCiclo'),
    path('Informe-Carrera/', InformeCarrera, name='InformeCarrera'),
    path('Recuperar-Contrasenia/', Recuperar, name='RecuperarContrasenia'),
    path('Reporte-Generado/', Reporte, name='ReporteGenerado'),
    path('Prediccion/', Prediccion, name='Prediccion'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
]