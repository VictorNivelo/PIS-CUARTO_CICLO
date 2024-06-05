from django.http import HttpResponse
from django.shortcuts import render

def PaginaPrincipal(request):
    return render(request, 'PaginaPrincipal.html')

def Hola(request):
    return render(request, 'HolaMundo.html')

def p(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

def full_width(request):
    return render(request, 'full-width.html')

def sidebar_left(request):
    return render(request, 'sidebar-left.html')

def sidebar_right(request):
    return render(request, 'sidebar-right.html')

def basic_grid(request):
    return render(request, 'basic-grid.html')

def Grafico(request):
    return render(request, 'Graficos.html')