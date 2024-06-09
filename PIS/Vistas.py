from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import RegistrarUsuarioForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError


def PaginaPrueba(request):
    return render(request, "PaginaPrueba.html")


def Hola(request):
    return render(request, "HolaMundo.html")


def PaginaPrincipal(request):
    return render(request, "Index.html")


def Galeria(request):
    return render(request, "Galeria.html")


def Informacion1(request):
    return render(request, "Informacion1.html")


def Informacion2(request):
    return render(request, "Informacion2.html")


def Informacion3(request):
    return render(request, "Informacion3.html")


def Informacion4(request):
    return render(request, "Informacion4.html")


def Grafico(request):
    return render(request, "Grafico.html")


def InformeMateria(request):
    return render(request, "InformeMateria.html")


def InformeCiclo(request):
    return render(request, "InformeCiclo.html")


def InformeCarrera(request):
    return render(request, "InformeCarrera.html")


def Recuperar(request):
    return render(request, "RecuperarContrasenia.html")


def Pagina_Administrador(request):
    return render(request, "PaginaAdministrador.html")


def Reporte(request):
    return render(request, "ReporteGenerado.html")


def Prediccion(request):
    return render(request, "Prediccion.html")


def PrediccionPresente(request):
    return render(request, "PrediccionPresente.html")


def registrar_usuario(request):
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["Contrasenia"])
            user.save()
            login(request, user)
            messages.success(request, "Usuario creado exitosamente.")
            return redirect("pagina_administrador")
        else:
            messages.error(request, "Error en la creación del usuario.")
    else:
        form = RegistrarUsuarioForm()
    return render(request, "RegistrarUsuario.html", {"form": form})


def iniciar_sesion(request):
    if request.method == "POST":
        correo = request.POST["txtCorreo"]
        password = request.POST["txtPassword"]
        user = authenticate(request, username=correo, password=password)
        if user is not None:
            login(request, user)
            return redirect("pagina_administrador")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect("iniciar_sesion")
    else:
        return render(request, "IniciarSesion.html")


# def signup(request):
#     if request.method == "GET":
#         return render(request, "RegistrarUsuario.html", {"form": UserCreationForm})
#     else:
#         if request.POST["password1"] == request.POST["password2"]:
#             try:
#                 user = User.objects.create_user(
#                     request.POST["username"], password=request.POST["password1"]
#                 )
#                 user.save()
#                 login(request, user)
#                 messages.success(request, "Usuario creado exitosamente.")
#                 return redirect("tasks")
#             except IntegrityError:
#                 return render(
#                     request,
#                     "RegistrarUsuario.html",
#                     {
#                         "form": UserCreationForm,
#                         "error": "El nombre de usuario ya existe.",
#                     },
#                 )
#         return render(
#             request,
#             "RegistrarUsuario.html",
#             {"form": UserCreationForm, "error": "La contraseña está incorrecta."},
#         )


# def signin(request):
#     if request.method == "GET":
#         return render(request, "IniciarSesion.html", {"form": AuthenticationForm})
#     else:
#         user = authenticate(
#             request,
#             username=request.POST["username"],
#             password=request.POST["password"],
#         )
#         if user is None:
#             return render(
#                 request,
#                 "IniciarSesion.html",
#                 {
#                     "form": AuthenticationForm,
#                     "error": "Usuario o contraseña incorrectos.",
#                 },
#             )

#         login(request, user)
#         return redirect("tasks")


# def pagina_administrador(request):
#     if request.session.get('logueado'):
#         return render(request, 'PaginaAdministrador.html')
#     else:
#         return redirect('iniciar_sesion')


# def registrar_usuario(request):
#     if request.method == "POST":
#         form = RegistrarUsuarioForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data["password"])
#             user.save()
#             login(request, user)
#             messages.success(request, "Usuario creado exitosamente.")
#             return redirect("pagina_administrador")
#         else:
#             messages.error(request, "Error en la creación del usuario.")
#     else:
#         form = RegistrarUsuarioForm()
#     return render(request, "RegistrarUsuario.html", {"form": form})
