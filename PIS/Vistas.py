from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from .forms import (
    InformeCarreraForm,
    InformeCicloForm,
    InformeMateriaForm,
    InicioSesionForm,
    ModificarRolUsuarioForm,
    RecuperarContraseniaForm,
    RegistrarUsuarioForm,
)


def PaginaPrincipal(request):
    return render(request, "Index.html")


@login_required
def Pagina_Administrador(request):
    return render(request, "PaginaAdministrador.html")


@login_required
def PaginaUsuario(request):
    return render(request, "PaginaDocente.html")


# Informacion del programa


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


# Informes


def InformeCiclo(request):
    if request.method == "POST":
        form = InformeCicloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Informe de ciclo guardado exitosamente.")
            return redirect("Index")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = InformeCicloForm()
    return render(request, "InformeCiclo.html", {"form": form})


def InformeCarrera(request):
    if request.method == "POST":
        form = InformeCarreraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Informe de carrera guardado exitosamente.")
            return redirect("Index")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = InformeCarreraForm()
    return render(request, "InformeCarrera.html", {"form": form})


def InformeMateria(request):
    if request.method == "POST":
        form = InformeMateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Informe de deserción estudiantil guardado exitosamente."
            )
            return redirect("Index")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = InformeMateriaForm()
    return render(request, "InformeMateria.html", {"form": form})


# Funciones del sistema


def Reporte(request):
    return render(request, "ReporteGenerado.html")


def Prediccion(request):
    return render(request, "Prediccion.html")


def PrediccionPresente(request):
    return render(request, "PrediccionPresente.html")


def Grafico(request):
    return render(request, "Grafico.html")


# Gestion de clases


def GestionUniversidad(request):
    return render(request, "GestionUniversidad.html")


def GestionFacultad(request):
    return render(request, "GestionFacultad.html")


def GestionCarrera(request):
    return render(request, "GestionCarrera.html")


def GestionCiclo(request):
    return render(request, "GestionCiclo.html")


def GestionMateria(request):
    return render(request, "GestionMateria.html")


# funciones de autenticacion


def RegistrarUsuario(request):
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.rol = "docente"
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect("Iniciar_Sesion")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "username":
                        messages.error(
                            request, f"Error en el nombre de usuario: {error}"
                        )
                    elif field == "password1":
                        messages.error(request, f"Contraseña no segura: {error}")
                    elif field == "password2":
                        messages.error(
                            request, f"Las contraseñas no coinciden: {error}"
                        )
                    else:
                        messages.error(request, f"Error en el campo {field}: {error}")
    else:
        form = RegistrarUsuarioForm()
    return render(request, "RegistrarUsuario.html", {"form": form})


def IniciarSesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Pagina_Usuario")
    else:
        form = AuthenticationForm()

    return render(request, "IniciarSesion.html", {"form": form})


@login_required
def CerrarSesion(request):
    logout(request)
    return redirect("IniciarSesion")


def RecuperarContrasenia(request):
    if request.method == "POST":
        form = RecuperarContraseniaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
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
