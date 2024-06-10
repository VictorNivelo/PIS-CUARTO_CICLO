from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from PIS.models import UsuarioPersonalizado
from .forms import InformeCarreraForm, InformeCicloForm, InformeMateriaForm, InicioSesionForm, RecuperarContraseniaForm, RegistrarUsuarioForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


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
    if request.method == 'POST':
        form = InformeCicloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informe de ciclo guardado exitosamente.')
            return redirect('Index') 
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario.')
    else:
        form = InformeCicloForm()
    return render(request, 'InformeCiclo.html', {'form': form})

def InformeCarrera(request):
    if request.method == 'POST':
        form = InformeCarreraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informe de carrera guardado exitosamente.')
            return redirect('Index') 
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario.')
    else:
        form = InformeCarreraForm()
    return render(request, 'InformeCarrera.html', {'form': form})


def InformeMateria(request):
    if request.method == 'POST':
        form = InformeMateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informe de deserción estudiantil guardado exitosamente.')
            return redirect('Index') 
        else:
            messages.error(request, 'Por favor, corrija los errores del formulario.')
    else:
        form = InformeMateriaForm()
    return render(request, 'InformeMateria.html', {'form': form})

# def InformeCarrera(request):
#     return render(request, "InformeCarrera.html")


def Reporte(request):
    return render(request, "ReporteGenerado.html")


def Prediccion(request):
    return render(request, "Prediccion.html")


def PrediccionPresente(request):
    return render(request, "PrediccionPresente.html")


@login_required
def Pagina_Administrador(request):
    return render(request, "PaginaAdministrador.html")


@login_required
def Pagina_Usuario(request):
    return render(request, "PaginaUsuario.html")


def RegistarUsuario(request):
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data["NombreUsuario"]
            correo = form.cleaned_data["Correo"]
            contrasenia = form.cleaned_data["Contrasenia"]
            confirmar_contrasenia = form.cleaned_data["Confirmar_Contrasenia"]
            if contrasenia == confirmar_contrasenia:
                try:
                    user = UsuarioPersonalizado.objects.create_user(
                        NombreUsuario=nombre_usuario, Correo=correo, Contrasenia=contrasenia
                    )
                    login(request, user)
                    messages.success(request, "Usuario creado exitosamente.")
                    return redirect("IniciarSesion")
                except IntegrityError:
                    return render(
                        request,
                        "RegistrarUsuario.html",
                        {
                            "form": form,
                            "error": "El nombre de usuario o correo electrónico ya existe.",
                        },
                    )
            else:
                return render(
                    request,
                    "RegistrarUsuario.html",
                    {
                        "form": form,
                        "error": "Las contraseñas no coinciden.",
                    },
                )
    else:
        form = RegistrarUsuarioForm()
    return render(request, "RegistrarUsuario.html", {"form": form})


# def RegistarUsuario(request):
#     if request.method == "GET":
#         return render(request, "RegistrarUsuario.html", {"form": RegistrarUsuarioForm})
#     else:
#         if request.POST["Contrasenia"] == request.POST["Confirmar_Contrasenia"]:
#             try:
#                 user = User.objects.create_user(
#                     request.POST["Correo"], password=request.POST["Contrasenia"]
#                 )
#                 user.save()
#                 login(request, user)
#                 messages.success(request, "Usuario creado exitosamente.")
#                 return redirect("IniciarSesion")
#             except IntegrityError:
#                 return render(
#                     request,
#                     "RegistrarUsuario.html",
#                     {
#                         "form": RegistrarUsuarioForm,
#                         "error": "El nombre de usuario ya existe.",
#                     },
#                 )


def IniciarSesion(request):
    if request.method == "GET":
        return render(request, "IniciarSesion.html", {"form": InicioSesionForm})
    else:
        user = authenticate(
            request,
            username=request.POST["Correo"],
            password=request.POST["Contrasenia"],
        )
        if user is not None:
            return render(
                request,
                "IniciarSesion.html",
                {
                    "form": InicioSesionForm,
                    "error": "Usuario o contraseña incorrectos.",
                },
            )

        login(request, user)
        return redirect("Pagina_Usuario")


@login_required
def CerrarSesion(request):
    logout(request)
    return redirect("IniciarSesion")


def Recuperar(request):
    if request.method == "POST":
        form = RecuperarContraseniaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            messages.success(
                request,
                "Se ha enviado un enlace de recuperación a su correo electrónico.",
            )
            return redirect("iniciar_sesion")
        else:
            messages.error(request, "Error al enviar el enlace de recuperación.")
    else:
        form = RecuperarContraseniaForm()
    return render(request, "RecuperarContrasenia.html", {"form": form})


# def registrar_usuario(request):
#     if request.method == "POST":
#         form = RegistrarUsuarioForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data["Contrasenia"])
#             user.save()
#             login(request, user)
#             messages.success(request, "Usuario creado exitosamente.")
#             return redirect("pagina_administrador")
#         else:
#             messages.error(request, "Error en la creación del usuario.")
#     else:
#         form = RegistrarUsuarioForm()
#     return render(request, "RegistrarUsuario.html", {"form": form})


# def iniciar_sesion(request):
#     if request.method == "POST":
#         form = InicioSesionForm(request.POST)
#         if form.is_valid():
#             correo = form.cleaned_data["Correo"]
#             password = form.cleaned_data["Contrasenia"]
#             user = authenticate(request, username=correo, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("pagina_administrador")
#             else:
#                 messages.error(request, "Usuario o contraseña incorrectos.")
#                 return redirect("iniciar_sesion")
#         else:
#             messages.error(request, "Error en el formulario de inicio de sesión.")
#             return redirect("iniciar_sesion")
#     else:
#         form = InicioSesionForm()
#     return render(request, "IniciarSesion.html", {"form": form})
