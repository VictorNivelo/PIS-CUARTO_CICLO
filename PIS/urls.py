from django.contrib import admin
from django.urls import path
from .Vistas import PaginaPrincipal, Hola, p, gallery, full_width, sidebar_left, sidebar_right, basic_grid, Grafico

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pr', PaginaPrincipal, name='PaginaPrincipal'),
    path('Hola/', Hola, name='Hola'),
    path('', p, name='index'),
    path('gallery/', gallery, name='gallery'),
    path('full-width/', full_width, name='full_width'),
    path('sidebar-left/', sidebar_left, name='sidebar_left'),
    path('sidebar-right/', sidebar_right, name='sidebar_right'),
    path('basic-grid/', basic_grid, name='basic_grid'),
    path('grafico/', Grafico, name='grafico'),
]