import token
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.utils.encoding import force_str
import re
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from docx import Document
import PyPDF2
import pdfplumber
import openpyxl
from datetime import datetime
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from django.shortcuts import render
from .models import Datos_Historicos
from .ModeloMatematico import model, params_list
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from PIS.models import (
    Genero,
    PeriodoAcademico,
    TipoDNI,
    Universidad,
    UsuarioPersonalizado,
    Facultad,
    Carrera,
    Ciclo,
    Materia,
    Genero,
    Estudiante,
)
from .forms import (
    GeneroForm,
    InformeCarreraForm,
    InformeCicloForm,
    InformeMateriaForm,
    PeriodoAcademicoForm,
    RecuperarContraseniaForm,
    RegistrarEstudianteForm,
    RegistrarUsuarioForm,
    UniversidadForm,
    FacultadForm,
    CarreraForm,
    CicloForm,
    MateriaForm,
    TipoDNIForm,
    CambiarContraseniaForm,
    InicioSesionForm,
)


def PaginaPrincipal(request):
    return render(request, "Index.html")


@login_required
def PaginaAdministrador(request):
    return render(request, "PaginaAdministrador.html")


@login_required
def PaginaDocente(request):
    return render(request, "PaginaDocente.html")


@login_required
def PaginaSecretaria(request):
    return render(request, "PaginaSecretaria.html")


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


def SubirImagenPerfil(request):
    if request.method == "POST":
        if request.FILES["Fotos"]:
            imagen = request.FILES["Fotos"]
            usuario = request.user
            usuario.foto = imagen
            usuario.save()
            messages.success(request, "Imagen de perfil actualizada exitosamente.")
        else:
            messages.error(request, "No se ha seleccionado ninguna imagen.")
    return redirect("Perfil_Usuario")


def RegistrarUsuario(request):
    if request.method == "POST":
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if UsuarioPersonalizado.objects.count() == 0:
                user.is_superuser = True
                user.is_staff = True
                user.rol = "Personal Administrativo"
            else:
                user.rol = "Docente"

            user.set_password(form.cleaned_data["password1"])
            user.save()
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

    return render(request, "RU-CrearUsuario.html", {"form": form})


def GestionUsuario(request):
    query = request.GET.get("search_query", "")
    filter_rol = request.GET.get("rol", "")
    filter_genero = request.GET.get("genero", "")
    filter_tipo_dni = request.GET.get("tipo_dni", "")

    usuarios = UsuarioPersonalizado.objects.all()
    generos = Genero.objects.all()
    tipos_dni = TipoDNI.objects.all()

    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) | Q(dni__icontains=query)
        )
    if filter_rol:
        usuarios = usuarios.filter(rol=filter_rol)
    if filter_genero:
        usuarios = usuarios.filter(genero_id=filter_genero)
    if filter_tipo_dni:
        usuarios = usuarios.filter(tipo_dni=filter_tipo_dni)

    if request.method == "POST":
        if "modify" in request.POST:
            user_id = request.POST.get("user_id")
            usuario = UsuarioPersonalizado.objects.get(id=user_id)
            usuario.username = request.POST.get("username")
            usuario.first_name = request.POST.get("first_name")
            usuario.last_name = request.POST.get("last_name")
            usuario.rol = request.POST.get("rol")
            usuario.genero_id = request.POST.get("genero")
            usuario.tipo_dni_id = request.POST.get("tipo_dni")
            usuario.dni = request.POST.get("dni")
            fecha_nacimiento_str = request.POST.get("fecha_nacimiento")
            try:
                fecha_nacimiento = datetime.strptime(
                    fecha_nacimiento_str, "%d/%m/%Y"
                ).date()
                usuario.fecha_nacimiento = fecha_nacimiento
            except ValueError:
                messages.error(
                    request,
                    "Formato de fecha de nacimiento inválido. Utiliza el formato dd/mm/aaaa.",
                )
                return redirect("Gestion_Usuario")
            usuario.telefono = request.POST.get("telefono")
            usuario.save()
            messages.success(
                request, "Información del usuario actualizada correctamente."
            )
        elif "delete" in request.POST:
            user_id = request.POST.get("user_id")
            usuario = UsuarioPersonalizado.objects.get(id=user_id)
            usuario.delete()
            messages.success(request, "Usuario eliminado correctamente.")
        return redirect("Gestion_Usuario")

    return render(
        request,
        "GestionUsuario.html",
        {
            "usuarios": usuarios,
            "query": query,
            "filter_rol": filter_rol,
            "filter_genero": filter_genero,
            "filter_tipo_dni": filter_tipo_dni,
            "generos": generos,
            "tipos_dni": tipos_dni,
        },
    )


def IniciarSesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.rol == "Personal Administrativo":
                    return redirect("Pagina_Administrador")
                elif user.rol == "Docente":
                    return redirect("Pagina_Docente")
                elif user.rol == "Secretaria":
                    return redirect("Pagina_Secretaria")
                else:
                    messages.error(request, "Rol de usuario no reconocido.")
                # return redirect("Pagina_Usuario")
    else:
        form = AuthenticationForm()

    return render(request, "IniciarSesion.html", {"form": form})


@login_required
def CerrarSesion(request):
    logout(request)
    return redirect("Iniciar_Sesion")


def RegistrarEstudiante(request):
    if request.method == "POST":
        form = RegistrarEstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante registrado exitosamente.")
            return redirect("Gestion_Estudiante")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
    else:
        form = RegistrarEstudianteForm()

    return render(request, "RE-CrearEstudiante.html", {"form": form})


def GestionEstudiante(request):
    query = request.GET.get("search_query", "")
    filter_genero = request.GET.get("genero", "")
    filter_modalidad = request.GET.get("modalidad_estudio", "")
    filter_tipo_educacion = request.GET.get("tipo_educacion", "")
    # filter_tipo_dni = request.GET.get("tipo_dni", "")

    estudiantes = Estudiante.objects.all()
    generos = Genero.objects.all()
    tipos_dni = TipoDNI.objects.all()
    materias = Materia.objects.all()

    if query:
        estudiantes = estudiantes.filter(
            Q(nombre_estudiante__icontains=query) | Q(dni_estudiante__icontains=query)
        )
    if filter_genero:
        estudiantes = estudiantes.filter(genero_id=filter_genero)
    # if filter_tipo_dni:
    #     estudiantes = estudiantes.filter(tipo_DNI=filter_tipo_dni)
    if filter_modalidad:
        estudiantes = estudiantes.filter(modalidad_estudio=filter_modalidad)
    if filter_tipo_educacion:
        estudiantes = estudiantes.filter(tipo_educacion=filter_tipo_educacion)

    if request.method == "POST":
        if "modify" in request.POST:
            estudiante_id = request.POST.get("estudiante_id")
            estudiante = Estudiante.objects.get(id=estudiante_id)
            estudiante.nombre_estudiante = request.POST.get("nombre_estudiante")
            estudiante.apellido_estudiante = request.POST.get("apellido_estudiante")
            estudiante.genero_id = request.POST.get("genero")
            estudiante.tipo_dni_id = request.POST.get("tipo_dni")
            estudiante.dni_estudiante = request.POST.get("dni_estudiante")
            estudiante.modalidad_estudio = request.POST.get("modalidad_estudio")
            estudiante.tipo_educacion = request.POST.get("tipo_educacion")
            estudiante.origen = request.POST.get("origen")
            estudiante.trabajo = request.POST.get("trabajo")
            estudiante.discapacidad = request.POST.get("discapacidad")
            estudiante.hijos = request.POST.get("hijos")
            materias_ids = request.POST.getlist("materia")
            estudiante.materia.set(materias_ids)
            estudiante.save()
            messages.success(
                request, "Información del estudiante actualizada correctamente."
            )
        elif "delete" in request.POST:
            estudiante_id = request.POST.get("estudiante_id")
            estudiante = Estudiante.objects.get(id=estudiante_id)
            estudiante.delete()
            messages.success(request, "Estudiante eliminado correctamente.")
        return redirect("Gestion_Estudiante")

    return render(
        request,
        "GestionEstudiante.html",
        {
            "estudiantes": estudiantes,
            "generos": generos,
            "tipos_dni": tipos_dni,
            "materias": materias,
            "query": query,
            "filter_genero": filter_genero,
            "filter_modalidad": filter_modalidad,
            "filter_tipo_educacion": filter_tipo_educacion,
            # "filter_tipo_dni": filter_tipo_dni,
        },
    )


# def RecuperarContrasenia(request):
#     if request.method == "POST":
#         form = RecuperarContraseniaForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             try:
#                 user = UsuarioPersonalizado.objects.get(username=username)
#             except UsuarioPersonalizado.DoesNotExist:
#                 messages.error(request, "El usuario no existe.")
#                 return render(request, "RecuperarContrasenia.html", {"form": form})

#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))

#             reset_url = reverse(
#                 "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
#             )

#             return redirect(reset_url)
#         else:
#             messages.error(request, "Error al enviar el enlace de recuperación.")
#     else:
#         form = RecuperarContraseniaForm()
#     return render(request, "RecuperarContrasenia.html", {"form": form})


# prueba 2


def CorreoEnviado(request, uidb64, token):
    return render(request, "CorreoRecuperacionEnviado.html")


User = get_user_model()


def RecuperarContrasenia(request):
    if request.method == "POST":
        form = RecuperarContraseniaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "El usuario no existe.")
                return render(request, "RecuperarContrasenia.html", {"form": form})

            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            return redirect("Correo_Enviado", uidb64=uidb64, token=token)
        else:
            messages.error(request, "Error al enviar el enlace de recuperación.")
    else:
        form = RecuperarContraseniaForm()
    return render(request, "RecuperarContrasenia.html", {"form": form})


def CambiarContrasenia(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = CambiarContraseniaForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data["Contrasenia"])
                user.save()
                messages.success(request, "Contraseña cambiada con éxito.")
                return redirect("Iniciar_Sesion")
        else:
            form = CambiarContraseniaForm()
        return render(request, "CambiarContrasenia.html", {"form": form})
    else:
        messages.error(
            request, "El enlace de restablecimiento de contraseña no es válido."
        )
        return redirect("Recuperar_Contrasenia")


# def RecuperarContrasenia(request):
#     if request.method == "POST":
#         form = RecuperarContraseniaForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             try:
#                 user = UsuarioPersonalizado.objects.get(username=username)
#             except UsuarioPersonalizado.DoesNotExist:
#                 messages.error(request, "El usuario no existe.")
#                 return render(request, "RecuperarContrasenia.html", {"form": form})

#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))

#             return render(
#                 request, "CambiarContrasenia.html", {"uid": uid, "token": token}
#             )
#         else:
#             messages.error(request, "Error al enviar el enlace de recuperación.")
#     else:
#         form = RecuperarContraseniaForm()
#     return render(request, "RecuperarContrasenia.html", {"form": form})


# User = get_user_model()

# def CambiarContrasenia(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         if request.method == "POST":
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Contraseña cambiada con éxito.')
#                 return redirect('Iniciar_Sesion')
#         else:
#             form = SetPasswordForm(user)
#         return render(request, 'CambiarContrasenia.html', {'form': form})
#     else:
#         messages.error(request, 'El enlace de restablecimiento de contraseña no es válido.')
#         return redirect('Recuperar_Contrasenia')


# User = get_user_model()


# def CambiarContrasenia(request):
#     if request.method == "POST":
#         uid = request.POST.get("uid")
#         token = request.POST.get("token")
#         new_password1 = request.POST.get("new_password1")
#         new_password2 = request.POST.get("new_password2")

#         if new_password1 != new_password2:
#             messages.error(request, "Las contraseñas no coinciden.")
#             return redirect("cambiar_contrasenia")

#         try:
#             uid = urlsafe_base64_decode(uid).decode()
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user is not None and default_token_generator.check_token(user, token):
#             user.password = make_password(new_password1)
#             user.save()
#             messages.success(request, "Contraseña cambiada con éxito.")
#             return redirect("Iniciar_Sesion")
#         else:
#             messages.error(
#                 request, "El enlace de restablecimiento de contraseña no es válido."
#             )
#             return redirect("Recuperar_Contrasenia")
#     else:
#         return render(request, "CambiarContrasenia.html")


# def RecuperarContrasenia(request):
#     if request.method == "POST":
#         form = RecuperarContraseniaForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             try:
#                 user = UsuarioPersonalizado.objects.get(username=username)
#             except UsuarioPersonalizado.DoesNotExist:
#                 messages.error(request, "El usuario no existe.")
#                 return render(request, "RecuperarContrasenia.html", {"form": form})

#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))

#             reset_url = reverse(
#                 "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
#             )
#             reset_url = request.build_absolute_uri(reset_url)

#             subject = "Recuperación de Contraseña"
#             message = render_to_string(
#                 "CambiarContrasenia.html",
#                 {
#                     "user": user,
#                     "reset_url": reset_url,
#                 },
#             )
#             from_email = settings.EMAIL_HOST_USER
#             to_email = form.cleaned_data["username"]
#             send_mail(subject, message, from_email, [to_email])

#             messages.success(
#                 request,
#                 "Se ha enviado un enlace de recuperación a su correo electrónico.",
#             )
#             return redirect("Iniciar_Sesion")
#         else:
#             messages.error(request, "Error al enviar el enlace de recuperación.")
#     else:
#         form = RecuperarContraseniaForm()
#     return render(request, "RecuperarContrasenia.html", {"form": form})


# def RecuperarContrasenia(request):
#     if request.method == "POST":
#         form = RecuperarContraseniaForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             messages.success(
#                 request,
#                 "Se ha enviado un enlace de recuperación a su correo electrónico.",
#             )
#             return redirect("Iniciar_Sesion")
#         else:
#             messages.error(request, "Error al enviar el enlace de recuperación.")
#     else:
#         form = RecuperarContraseniaForm()
#     return render(request, "RecuperarContrasenia.html", {"form": form})


# def CambiarContrasenia(request):
#     if request.method == "POST":
#         form = CambiarContraseniaForm(request.POST)
#         if form.is_valid():
#             nueva_contrasenia = form.cleaned_data["Contrasenia"]
#             request.user.set_password(nueva_contrasenia)
#             request.user.save()
#             update_session_auth_hash(request, request.user)
#             messages.success(request, "Contraseña cambiada exitosamente.")
#             return redirect("Iniciar_Sesion")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#     else:
#         form = CambiarContraseniaForm()

#     return render(request, "CambiarContrasenia.html", {"form": form})


def RegistrarTipoDNI(request):
    if request.method == "POST":
        form = TipoDNIForm(request.POST)
        if form.is_valid():
            tipo_dni = form.save(commit=False)
            tipo_dni.save()
            messages.success(request, "Tipo de DNI registrado exitosamente.")
            return redirect("Gestion_TipoDNI")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = TipoDNIForm()
    return render(request, "RTD-CrearTipoDNI.html", {"form": form})


def GestionTipoDNI(request):
    query = request.GET.get("search_query", "")
    tipos_dni = TipoDNI.objects.all()

    if query:
        tipos_dni = tipos_dni.filter(Q(nombre_tipo_dni__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            tipo_dni_id = request.POST.get("tipo_dni_id")
            tipo_dni = TipoDNI.objects.get(id=tipo_dni_id)
            tipo_dni.nombre_tipo_dni = request.POST.get("nombre_tipo_dni")
            tipo_dni.descripcion_tipo_dni = request.POST.get("descripcion_tipo_dni")
            tipo_dni.save()
            messages.success(request, "Tipo de DNI actualizado exitosamente.")
        elif "delete" in request.POST:
            tipo_dni_id = request.POST.get("tipo_dni_id")
            tipo_dni = TipoDNI.objects.get(id=tipo_dni_id)
            tipo_dni.delete()
            messages.success(request, "Tipo de DNI eliminado exitosamente.")
        return redirect("Gestion_TipoDNI")

    return render(
        request, "GestionTipoDNI.html", {"tipos_dni": tipos_dni, "query": query}
    )


def RegistrarGenero(request):
    if request.method == "POST":
        form = GeneroForm(request.POST)
        if form.is_valid():
            genero = form.save(commit=False)
            genero.save()
            messages.success(request, "Género registrado exitosamente.")
            return redirect("Gestion_Genero")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = GeneroForm()
        # messages.success(request, "Género registrado exitosamente.")
        # return redirect("Gestion_Genero")
    return render(request, "RG-CrearGenero.html", {"form": form})


def GestionGenero(request):
    query = request.GET.get("search_query", "")
    generos = Genero.objects.all()

    if query:
        generos = generos.filter(Q(nombre_genero__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            genero_id = request.POST.get("genero_id")
            genero = Genero.objects.get(id=genero_id)
            genero.nombre_genero = request.POST.get("nombre_genero")
            genero.descripcion_genero = request.POST.get("descripcion_genero")
            genero.save()
            messages.success(request, "Género actualizado exitosamente.")
        elif "delete" in request.POST:
            genero_id = request.POST.get("genero_id")
            genero = Genero.objects.get(id=genero_id)
            genero.delete()
            messages.success(request, "Género eliminado exitosamente.")
        return redirect("Gestion_Genero")

    return render(request, "GestionGenero.html", {"generos": generos, "query": query})


def RegistrarUniversidad(request):
    if request.method == "POST":
        form = UniversidadForm(request.POST)
        if form.is_valid():
            universidad = form.save(commit=False)
            universidad.save()
            messages.success(request, "Universidad registrada exitosamente.")
            return redirect("Gestion_Universidad")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = UniversidadForm()

    return render(request, "RU-CrearUniversidad.html", {"form": form})


def GestionUniversidad(request):
    query = request.GET.get("search_query", "")

    universidades = Universidad.objects.all()

    if query:
        universidades = universidades.filter(
            Q(nombre_universidad__icontains=query)
            | Q(correo_universidad__icontains=query)
        )

    if request.method == "POST":
        if "modify" in request.POST:
            universidad_id = request.POST.get("universidad_id")
            universidad = Universidad.objects.get(id=universidad_id)
            universidad.nombre_universidad = request.POST.get("nombre_universidad")
            universidad.direccion_universidad = request.POST.get(
                "direccion_universidad"
            )
            universidad.telefono_universidad = request.POST.get("telefono_universidad")
            universidad.correo_universidad = request.POST.get("correo_universidad")
            fecha_fundacion_str = request.POST.get("fecha_fundacion")
            try:
                fecha_fundacion = datetime.strptime(
                    fecha_fundacion_str, "%Y-%m-%d"
                ).date()
                universidad.fecha_fundacion = fecha_fundacion
            except ValueError:
                messages.error(
                    request,
                    "Formato de fecha de nacimiento inválido. Utiliza el formato dd/mm/aaaa.",
                )
            universidad.save()
            messages.success(request, "Universidad actualizada exitosamente.")
        elif "delete" in request.POST:
            universidad_id = request.POST.get("universidad_id")
            universidad = Universidad.objects.get(id=universidad_id)
            universidad.delete()
            messages.success(request, "Universidad eliminada exitosamente.")
        return redirect("Gestion_Universidad")

    return render(
        request,
        "GestionUniversidad.html",
        {
            "universidades": universidades,
            "query": query,
        },
    )


def RegistrarFacultad(request):
    if request.method == "POST":
        form = FacultadForm(request.POST)
        if form.is_valid():
            facultad = form.save(commit=False)
            facultad.save()
            messages.success(request, "Facultad registrada exitosamente.")
            return redirect("Gestion_Facultad")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = FacultadForm()

    return render(request, "RF-CrearFacultad.html", {"form": form})


def GestionFacultad(request):
    query = request.GET.get("search_query", "")
    facultades = Facultad.objects.all()
    universidades = Universidad.objects.all()

    if query:
        facultades = facultades.filter(Q(nombre_facultad__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            facultad_id = request.POST.get("facultad_id")
            facultad = Facultad.objects.get(id=facultad_id)
            facultad.nombre_facultad = request.POST.get("nombre_facultad")

            fecha_fundacion_str = request.POST.get("fecha_fundacion")
            try:
                fecha_fundacion = datetime.strptime(
                    fecha_fundacion_str, "%Y-%m-%d"
                ).date()
                facultad.fecha_fundacion = fecha_fundacion
            except ValueError:
                messages.error(
                    request,
                    "Formato de fecha de fundación inválido. Utiliza el formato dd/mm/aaaa.",
                )
                return redirect("Gestion_Facultad")

            universidad_id = request.POST.get("universidad")
            universidad = Universidad.objects.get(id=universidad_id)
            facultad.universidad = universidad
            facultad.save()
            messages.success(request, "Facultad actualizada exitosamente.")
        elif "delete" in request.POST:
            facultad_id = request.POST.get("facultad_id")
            facultad = Facultad.objects.get(id=facultad_id)
            facultad.delete()
            messages.success(request, "Facultad eliminada exitosamente.")
        return redirect("Gestion_Facultad")

    return render(
        request,
        "GestionFacultad.html",
        {
            "facultades": facultades,
            "universidades": universidades,
            "query": query,
        },
    )


def RegistrarCarrera(request):
    if request.method == "POST":
        form = CarreraForm(request.POST)
        if form.is_valid():
            carrera = form.save(commit=False)
            carrera.save()
            messages.success(request, "Carrera registrada exitosamente.")
            return redirect("Gestion_Carrera")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = CarreraForm()

    return render(request, "RC-CrearCarrera.html", {"form": form})


def GestionCarrera(request):
    query = request.GET.get("search_query", "")
    carreras = Carrera.objects.all()
    facultades = Facultad.objects.all()

    if query:
        carreras = carreras.filter(Q(nombre_carrera__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            carrera_id = request.POST.get("carrera_id")
            carrera = Carrera.objects.get(id=carrera_id)
            carrera.nombre_carrera = request.POST.get("nombre_carrera")
            carrera.duracion = request.POST.get("duracion")
            facultad_id = request.POST.get("facultad")
            facultad = Facultad.objects.get(id=facultad_id)
            carrera.facultad = facultad
            carrera.save()
            messages.success(request, "Carrera actualizada exitosamente.")
        elif "delete" in request.POST:
            carrera_id = request.POST.get("carrera_id")
            carrera = Carrera.objects.get(id=carrera_id)
            carrera.delete()
            messages.success(request, "Carrera eliminada exitosamente.")
        return redirect("Gestion_Carrera")

    return render(
        request,
        "GestionCarrera.html",
        {
            "carreras": carreras,
            "facultades": facultades,
            "query": query,
        },
    )


def RegistrarCiclo(request):
    if request.method == "POST":
        form = CicloForm(request.POST)
        if form.is_valid():
            ciclo = form.save(commit=False)
            ciclo.save()
            messages.success(request, "Ciclo registrado exitosamente.")
            return redirect("Gestion_Ciclo")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = CicloForm()

    return render(request, "RC-CrearCiclo.html", {"form": form})


def GestionCiclo(request):
    query = request.GET.get("search_query", "")
    ciclos = Ciclo.objects.all()
    carreras = Carrera.objects.all()

    if query:
        ciclos = ciclos.filter(Q(nombre_ciclo__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            ciclo_id = request.POST.get("ciclo_id")
            ciclo = Ciclo.objects.get(id=ciclo_id)
            ciclo.nombre_ciclo = request.POST.get("nombre_ciclo")
            ciclo.numero_ciclo = request.POST.get("numero_ciclo")
            fecha_inicio_str = request.POST.get("fecha_inicio")
            if fecha_inicio_str:
                try:
                    fecha_fundacion = datetime.strptime(
                        fecha_inicio_str, "%Y-%m-%d"
                    ).date()
                    ciclo.fecha_fundacion = fecha_fundacion
                except ValueError:
                    messages.error(
                        request,
                        "Formato de fecha de fundación inválido. Utiliza el formato dd/mm/aaaa.",
                    )
                    return redirect("Gestion_Facultad")
            if fecha_inicio_str:
                try:
                    fecha_inicio = datetime.strptime(
                        fecha_inicio_str, "%Y-%m-%d"
                    ).date()
                    ciclo.fecha_inicio = fecha_inicio
                except ValueError:
                    messages.error(
                        request,
                        "Formato de fecha de inicio inválido. Utiliza el formato dd/mm/aaaa.",
                    )
                    return redirect("Gestion_Ciclo")
            fecha_fin_str = request.POST.get("fecha_fin")
            if fecha_fin_str:
                try:
                    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
                    ciclo.fecha_fin = fecha_fin
                except ValueError:
                    messages.error(
                        request,
                        "Formato de fecha de fin inválido. Utiliza el formato dd/mm/aaaa.",
                    )
                    return redirect("Gestion_Ciclo")
            carrera_id = request.POST.get("carrera")
            carrera = Carrera.objects.get(id=carrera_id)
            ciclo.carrera = carrera
            ciclo.save()
            messages.success(request, "Ciclo actualizado exitosamente.")
        elif "delete" in request.POST:
            ciclo_id = request.POST.get("ciclo_id")
            ciclo = Ciclo.objects.get(id=ciclo_id)
            ciclo.delete()
            messages.success(request, "Ciclo eliminado exitosamente.")
        return redirect("Gestion_Ciclo")

    return render(
        request,
        "GestionCiclo.html",
        {
            "ciclos": ciclos,
            "carreras": carreras,
            "query": query,
        },
    )


def RegistrarPeriodoAcademico(request):
    if request.method == "POST":
        form = PeriodoAcademicoForm(request.POST)
        if form.is_valid():
            periodo_academico = form.save(commit=False)
            periodo_academico.save()
            messages.success(request, "Periodo académico registrado exitosamente.")
            return redirect("Gestion_PeriodoAcademico")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = PeriodoAcademicoForm()

    return render(request, "RPA-CrearPeriodoAcademico.html", {"form": form})


def GestionPeriodoAcademico(request):
    query = request.GET.get("search_query", "")
    PeriodosAcademicos = PeriodoAcademico.objects.all()

    if query:
        PeriodosAcademicos = PeriodosAcademicos.filter(
            Q(codigo_periodo_academico__icontains=query)
        )

    if request.method == "POST":
        if "modify" in request.POST:
            periodo_academico_id = request.POST.get("PeriodoAcademico_id")
            periodo_academico = PeriodoAcademico.objects.get(id=periodo_academico_id)
            periodo_academico.codigo_periodo_academico = request.POST.get(
                "codigo_periodo_academico"
            )
            fecha_inicio_str = request.POST.get("fecha_inicio")
            if fecha_inicio_str:
                try:
                    fecha_inicio = datetime.strptime(
                        fecha_inicio_str, "%Y-%m-%d"
                    ).date()
                    periodo_academico.fecha_inicio = fecha_inicio
                except ValueError:
                    messages.error(
                        request,
                        "Formato de fecha de inicio inválido. Utiliza el formato dd/mm/aaaa.",
                    )
                    return redirect("Gestion_PeriodoAcademico")
            fecha_fin_str = request.POST.get("fecha_fin")
            if fecha_fin_str:
                try:
                    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
                    periodo_academico.fecha_fin = fecha_fin
                except ValueError:
                    messages.error(
                        request,
                        "Formato de fecha de fin inválido. Utiliza el formato dd/mm/aaaa.",
                    )
                    return redirect("Gestion_PeriodoAcademico")
            periodo_academico.estado_periodo_academico = request.POST.get("estado")
            periodo_academico.save()
            messages.success(request, "Periodo académico actualizado exitosamente.")
        elif "delete" in request.POST:
            periodo_academico_id = request.POST.get("PeriodoAcademico_id")
            periodo_academico = PeriodoAcademico.objects.get(id=periodo_academico_id)
            periodo_academico.delete()
            messages.success(request, "Periodo académico eliminado exitosamente.")
        return redirect("Gestion_PeriodoAcademico")

    return render(
        request,
        "GestionPeriodoAcademico.html",
        {"periodosAcademicos": PeriodosAcademicos, "query": query},
    )


def RegistrarMateria(request):
    if request.method == "POST":
        form = MateriaForm(request.POST)
        if form.is_valid():
            materia = form.save(commit=False)
            materia.save()
            messages.success(request, "Materia registrada exitosamente.")
            return redirect("Gestion_Materia")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = MateriaForm()

    return render(request, "RM-CrearMateria.html", {"form": form})


def GestionMateria(request):
    query = request.GET.get("search_query", "")
    materias = Materia.objects.all()
    ciclos = Ciclo.objects.all()
    docentes = UsuarioPersonalizado.objects.filter(rol="Docente")

    if query:
        materias = materias.filter(Q(nombre_materia__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            materia_id = request.POST.get("materia_id")
            materia = Materia.objects.get(id=materia_id)
            materia.nombre_materia = request.POST.get("nombre_materia")
            materia.save()
            messages.success(request, "Materia actualizada exitosamente.")
        elif "delete" in request.POST:
            materia_id = request.POST.get("materia_id")
            materia = Materia.objects.get(id=materia_id)
            materia.delete()
            messages.success(request, "Materia eliminada exitosamente.")
        return redirect("Gestion_Materia")

    return render(
        request,
        "GestionMateria.html",
        {
            "materias": materias,
            "docentes": docentes,
            "ciclos": ciclos,
            "query": query,
        },
    )


# Funcionalidad de subir archivo para su procesamiento


# def Extraer_DOCS(file):
#     document = Document(file)
#     data = {}
#     for para in document.paragraphs:
#         text = para.text.strip()
#         if "Materia:" in text:
#             data["materia"] = text.replace("Materia:", "").strip()
#         elif "Docente encargado:" in text:
#             data["docente_encargado"] = text.replace("Docente encargado:", "").strip()
#         elif "Numero de estudiante:" in text:
#             data["numero_estudiantes"] = int(
#                 text.replace("Numero de estudiante:", "").strip()
#             )
#         elif "Aprobados:" in text:
#             data["aprobados"] = int(text.replace("Aprobados:", "").strip())
#         elif "Reprobados:" in text:
#             data["reprobados"] = int(text.replace("Reprobados:", "").strip())
#         elif "Desertores:" in text:
#             data["desertores"] = int(text.replace("Desertores:", "").strip())
#         elif "Retirados:" in text:
#             data["retirados"] = int(text.replace("Retirados:", "").strip())
#     return data


# def Extraer_PDF(file):
#     data = {}
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             if text:
#                 for line in text.split("\n"):
#                     line = line.strip()
#                     if "Materia:" in line:
#                         data["materia"] = line.replace("Materia:", "").strip()
#                     elif "Docente encargado:" in line:
#                         data["docente_encargado"] = line.replace(
#                             "Docente encargado:", ""
#                         ).strip()
#                     elif "Numero de estudiante:" in line:
#                         data["numero_estudiantes"] = int(
#                             line.replace("Numero de estudiante:", "").strip()
#                         )
#                     elif "Aprobados:" in line:
#                         data["aprobados"] = int(line.replace("Aprobados:", "").strip())
#                     elif "Reprobados:" in line:
#                         data["reprobados"] = int(
#                             line.replace("Reprobados:", "").strip()
#                         )
#                     elif "Desertores:" in line:
#                         data["desertores"] = int(
#                             line.replace("Desertores:", "").strip()
#                         )
#                     elif "Retirados:" in line:
#                         data["retirados"] = int(line.replace("Retirados:", "").strip())
#     return data

# valido
# def Extraer_XLSX(file):
#     data = {}
#     workbook = openpyxl.load_workbook(file, data_only=True)
#     sheet = workbook.active

#     for row in sheet.iter_rows(min_row=1, max_col=7, values_only=True):
#         for cell_value in row:
#             if isinstance(cell_value, str):
#                 if "Materia:" in cell_value:
#                     data["materia"] = cell_value.replace("Materia:", "").strip()
#                 elif "Docente encargado:" in cell_value:
#                     data["docente_encargado"] = cell_value.replace("Docente encargado:", "").strip()
#             elif isinstance(cell_value, (int, float)):
#                 if "Numero de estudiante:" in str(cell_value):
#                     data["numero_estudiantes"] = int(str(cell_value).replace("Numero de estudiante:", "").strip())
#                 elif "Aprobados:" in str(cell_value):
#                     data["aprobados"] = int(str(cell_value).replace("Aprobados:", "").strip())
#                 elif "Reprobados:" in str(cell_value):
#                     data["reprobados"] = int(str(cell_value).replace("Reprobados:", "").strip())
#                 elif "Desertores:" in str(cell_value):
#                     data["desertores"] = int(str(cell_value).replace("Desertores:", "").strip())
#                 elif "Retirados:" in str(cell_value):
#                     data["retirados"] = int(str(cell_value).replace("Retirados:", "").strip())

#     workbook.close()
#     return data

# def Extraer_XLSX(file):
#     data = {}
#     workbook = openpyxl.load_workbook(file)
#     sheet = workbook.active

#     for row in sheet.iter_rows(values_only=True):
#         for cell_value in row:
#             if isinstance(cell_value, str):
#                 if "Materia:" in cell_value:
#                     data["materia"] = cell_value.replace("Materia:", "").strip()
#                 elif "Docente encargado:" in cell_value:
#                     data["docente_encargado"] = cell_value.replace(
#                         "Docente encargado:", ""
#                     ).strip()
#             elif isinstance(cell_value, (int, float)):
#                 if "Numero de estudiante:" in str(cell_value):
#                     data["numero_estudiantes"] = int(
#                         str(cell_value).replace("Numero de estudiante:", "").strip()
#                     )
#                 elif "Aprobados:" in str(cell_value):
#                     data["aprobados"] = int(
#                         str(cell_value).replace("Aprobados:", "").strip()
#                     )
#                 elif "Reprobados:" in str(cell_value):
#                     data["reprobados"] = int(
#                         str(cell_value).replace("Reprobados:", "").strip()
#                     )
#                 elif "Desertores:" in str(cell_value):
#                     data["desertores"] = int(
#                         str(cell_value).replace("Desertores:", "").strip()
#                     )
#                 elif "Retirados:" in str(cell_value):
#                     data["retirados"] = int(
#                         str(cell_value).replace("Retirados:", "").strip()
#                     )

#     return data


# def CargarInforme(request):
#     if request.method == "POST":
#         file = request.FILES["document"]
#         file_extension = file.name.split(".")[-1].lower()

#         if file_extension == "docx":
#             data = Extraer_DOCS(file)
#         elif file_extension == "pdf":
#             data = Extraer_PDF(file)
#         elif file_extension == "xlsx":
#             data = Extraer_XLSX(file)
#         else:
#             return HttpResponse("Formato de archivo no soportado.", status=400)

#         form = InformeMateriaForm(initial=data)
#         return render(request, "InformeMateria.html", {"form": form})

#     return render(request, "CargarInforme.html")


# def Extraer_PDF(file):
#     data = []
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             text = page.extract_text()
#             if text:
#                 current_item = {}
#                 for line in text.split("\n"):
#                     if line.startswith("Universidad:"):
#                         if current_item:
#                             data.append(current_item)
#                         current_item = {"tipo": "universidad", "datos": {}}
#                         current_item["datos"]["nombre_universidad"] = line.replace(
#                             "Universidad:", ""
#                         ).strip()
#                     elif line.startswith("Dirección:"):
#                         current_item["datos"]["direccion_universidad"] = line.replace(
#                             "Dirección:", ""
#                         ).strip()
#                     elif line.startswith("Teléfono:"):
#                         current_item["datos"]["telefono_universidad"] = line.replace(
#                             "Teléfono:", ""
#                         ).strip()
#                     elif line.startswith("Correo:"):
#                         current_item["datos"]["correo_universidad"] = line.replace(
#                             "Correo:", ""
#                         ).strip()
#                     elif line.startswith("Fecha de fundación:"):
#                         current_item["datos"]["fecha_fundacion"] = line.replace(
#                             "Fecha de fundación:", ""
#                         ).strip()
#                 if current_item:
#                     data.append(current_item)
#     return data


# def Extraer_XLSX(file):
#     data = []
#     workbook = openpyxl.load_workbook(file)
#     sheet = workbook.active
#     headers = [cell.value for cell in sheet[1]]

#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         item = {"tipo": row[0], "datos": {}}
#         for header, value in zip(headers[1:], row[1:]):
#             if value:
#                 item["datos"][header.lower().replace(" ", "_")] = value
#         data.append(item)

#     return data


# def Extraer_DOCS(file):
#     document = Document(file)
#     data = []
#     current_item = None

#     for para in document.paragraphs:
#         text = para.text.strip()
#         if text.startswith("Universidad:"):
#             if current_item:
#                 data.append(current_item)
#             current_item = {"tipo": "universidad", "datos": {}}
#             current_item["datos"]["nombre_universidad"] = text.replace(
#                 "Universidad:", ""
#             ).strip()
#         elif text.startswith("Direccion:"):
#             current_item["datos"]["direccion_universidad"] = text.replace(
#                 "Direccion:", ""
#             ).strip()
#         elif text.startswith("Telefono:"):
#             current_item["datos"]["telefono_universidad"] = text.replace(
#                 "Telefono:", ""
#             ).strip()
#         elif text.startswith("Correo:"):
#             current_item["datos"]["correo_universidad"] = text.replace(
#                 "Correo:", ""
#             ).strip()
#         elif text.startswith("Fecha de fundación:"):
#             current_item["datos"]["fecha_fundacion"] = text.replace(
#                 "Fecha de fundación:", ""
#             ).strip()

#     if current_item:
#         data.append(current_item)

#     return data


# def CargarInforme(request):
#     if request.method == "POST" and request.FILES["document"]:
#         file = request.FILES["document"]
#         file_extension = file.name.split(".")[-1].lower()

#         path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
#         tmp_file = os.path.join(settings.MEDIA_ROOT, path)

#         try:
#             if file_extension == "docx":
#                 data = Extraer_DOCS(tmp_file)
#             elif file_extension == "pdf":
#                 data = Extraer_PDF(tmp_file)
#             elif file_extension in ["xlsx", "xls"]:
#                 data = Extraer_XLSX(tmp_file)
#             else:
#                 return HttpResponse("Formato de archivo no soportado.", status=400)

#             for item in data:
#                 if item["tipo"] == "universidad":
#                     Universidad.objects.create(**item["datos"])

#             messages.success(request, "Universidades importadas exitosamente.")
#             return JsonResponse({"success": True})

#         except Exception as e:
#             messages.error(request, f"Error al importar universidades: {str(e)}")
#             return JsonResponse({"success": False, "error": str(e)})

#         finally:
#             default_storage.delete(tmp_file)

#     return render(request, "CargarInforme.html")


# def CargarInforme(request):
#     if request.method == "POST" and request.FILES["document"]:
#         file = request.FILES["document"]
#         file_extension = file.name.split(".")[-1].lower()

#         path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
#         tmp_file = os.path.join(settings.MEDIA_ROOT, path)

#         try:
#             if file_extension == "docx":
#                 data = Extraer_DOCS(tmp_file)
#             elif file_extension == "pdf":
#                 data = Extraer_PDF(tmp_file)
#             elif file_extension in ["xlsx", "xls"]:
#                 data = Extraer_XLSX(tmp_file)
#             else:
#                 return HttpResponse("Formato de archivo no soportado.", status=400)

#             for item in data:
#                 if "tipo" in item:
#                     if item["tipo"] == "universidad":
#                         Universidad.objects.create(**item["datos"])
#                     elif item["tipo"] == "facultad":
#                         Facultad.objects.create(**item["datos"])
#                     elif item["tipo"] == "carrera":
#                         Carrera.objects.create(**item["datos"])
#                     elif item["tipo"] == "ciclo":
#                         Ciclo.objects.create(**item["datos"])
#                     elif item["tipo"] == "materia":
#                         Materia.objects.create(**item["datos"])

#             messages.success(request, "Datos importados exitosamente.")
#             return redirect("Index")

#         finally:
#             default_storage.delete(tmp_file)

#     return render(request, "CargarInforme.html")


@csrf_exempt
def upload_universities(request):
    if request.method == "POST" and request.FILES.get("document"):
        document = request.FILES["document"]
        content = document.read().decode("utf-8")

        universities = parse_university_data(content)
        for university in universities:
            Universidad.objects.create(**university)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def parse_university_data(content):
    pattern = re.compile(
        r"Universidad:\s*(.*?)\s*Direccion:\s*(.*?)\s*Telefono:\s*(.*?)\s*Correo:\s*(.*?)\s*Fecha de fundación:\s*(.*?)\s*(?=Universidad:|$)"
    )
    matches = pattern.findall(content)

    universities = []
    for match in matches:
        universities.append(
            {
                "nombre_universidad": match[0],
                "direccion_universidad": match[1],
                "telefono_universidad": match[2],
                "correo_universidad": match[3],
                "fecha_fundacion": match[4],
            }
        )

    return universities


ENTITY_MAPPING = {
    "universidad": Universidad,
    "facultad": Facultad,
    "carrera": Carrera,
    "ciclo": Ciclo,
    "materia": Materia,
    "usuario": UsuarioPersonalizado,
}


def extract_data_from_file(file, file_extension):
    if file_extension == "docx":
        return extract_docs(file)
    elif file_extension == "pdf":
        return extract_pdf(file)
    elif file_extension in ["xlsx", "xls"]:
        return extract_xlsx(file)
    else:
        raise ValueError("Unsupported file format")


def extract_pdf(file):
    data = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                current_item = {}
                for line in text.split("\n"):
                    key, value = map(str.strip, line.split(":", 1))
                    if key.lower() in ENTITY_MAPPING:
                        if current_item:
                            data.append(current_item)
                        current_item = {"tipo": key.lower(), "datos": {}}
                    if current_item:
                        current_item["datos"][key.lower().replace(" ", "_")] = value
                if current_item:
                    data.append(current_item)
    return data


def extract_xlsx(file):
    data = []
    workbook = openpyxl.load_workbook(file)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        item = {"tipo": row[0].lower(), "datos": {}}
        for header, value in zip(headers[1:], row[1:]):
            if value:
                item["datos"][header.lower().replace(" ", "_")] = value
        data.append(item)

    return data


def extract_docs(file):
    document = Document(file)
    data = []
    current_item = None

    for para in document.paragraphs:
        text = para.text.strip()
        if ":" in text:
            key, value = map(str.strip, text.split(":", 1))
            if key.lower() in ENTITY_MAPPING:
                if current_item:
                    data.append(current_item)
                current_item = {"tipo": key.lower(), "datos": {}}
            if current_item:
                current_item["datos"][key.lower().replace(" ", "_")] = value

    if current_item:
        data.append(current_item)

    return data


def save_entities(data):
    for item in data:
        model = ENTITY_MAPPING.get(item["tipo"])
        if model:
            model.objects.create(**item["datos"])
        else:
            print(f"Unrecognized entity type: {item['tipo']}")


def CargarInforme(request):
    if request.method == "POST" and request.FILES["document"]:
        file = request.FILES["document"]
        file_extension = file.name.split(".")[-1].lower()

        path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        try:
            data = extract_data_from_file(tmp_file, file_extension)
            save_entities(data)
            messages.success(request, "Datos importados exitosamente.")
            return redirect("Index")
        except Exception as e:
            messages.error(request, f"Error al importar datos: {str(e)}")
        finally:
            default_storage.delete(tmp_file)

    return render(request, "CargarInforme.html")


def upload_universities(request):
    if request.method == "POST":
        file = request.FILES["file"]

        try:
            content = file.read().decode("utf-8")

            universities = content.strip().split("\n\n")

            for uni_data in universities:
                nombre = re.search(r"Universidad:\s*(.*)", uni_data).group(1)
                direccion = re.search(r"Direccion:\s*(.*)", uni_data).group(1)
                telefono = re.search(r"Telefono:\s*(.*)", uni_data).group(1)
                correo = re.search(r"Correo:\s*(.*)", uni_data).group(1)
                fecha_fundacion = re.search(
                    r"Fecha de fundación:\s*(.*)", uni_data
                ).group(1)

                universidad, created = Universidad.objects.get_or_create(
                    nombre_universidad=nombre,
                    defaults={
                        "direccion_universidad": direccion,
                        "telefono_universidad": telefono,
                        "correo_universidad": correo,
                        "fecha_fundacion": fecha_fundacion,
                    },
                )
                if not created:
                    universidad.direccion_universidad = direccion
                    universidad.telefono_universidad = telefono
                    universidad.correo_universidad = correo
                    universidad.fecha_fundacion = fecha_fundacion
                    universidad.save()

        except UnicodeDecodeError as e:
            return render(
                request,
                "upload.html",
                {"error": f"Error de codificación del archivo: {e}"},
            )
        except Exception as e:
            return render(
                request, "upload.html", {"error": f"Error procesando el archivo: {e}"}
            )

    return render(request, "upload.html")


# @csrf_exempt
# def upload_universities(request):
#     if request.method == "POST" and request.FILES.get("document"):
#         document = request.FILES["document"]
#         content = document.read().decode("utf-8")

#         universities = parse_university_data(content)
#         for university in universities:
#             Universidad.objects.create(**university)

#         return JsonResponse({"success": True})

#     return JsonResponse({"success": False})

# def parse_university_data(content):
#     pattern = re.compile(
#         r"Universidad:\s*(.*?)\s*Direccion:\s*(.*?)\s*Telefono:\s*(.*?)\s*Correo:\s*(.*?)\s*Fecha de fundación:\s*(.*?)\s*(?=Universidad:|$)"
#     )
#     matches = pattern.findall(content)

#     universities = []
#     for match in matches:
#         universities.append(
#             {
#                 "nombre_universidad": match[0],
#                 "direccion_universidad": match[1],
#                 "telefono_universidad": match[2],
#                 "correo_universidad": match[3],
#                 "fecha_fundacion": match[4],
#             }
#         )

#     return universities


# def parse_university_data(content):
#     pattern = re.compile(
#         r"Universidad:\s*(.*?)\s*Direccion:\s*(.*?)\s*Telefono:\s*(.*?)\s*Correo:\s*(.*?)\s*Fecha de fundación:\s*(.*?)\s*(?=Universidad:|$)"
#     )
#     matches = pattern.findall(content)

#     universities = []
#     for match in matches:
#         universities.append(
#             {
#                 "nombre_universidad": match[0],
#                 "direccion_universidad": match[1],
#                 "telefono_universidad": match[2],
#                 "correo_universidad": match[3],
#                 "fecha_fundacion": match[4],
#             }
#         )

#     return universities


# @csrf_exempt
# def upload_universities(request):
#     if request.method == "POST" and request.FILES.get("document"):
#         file = request.FILES["document"]
#         file_extension = file.name.split(".")[-1].lower()

#         path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
#         tmp_file = os.path.join(settings.MEDIA_ROOT, path)

#         try:
#             if file_extension == "docx":
#                 data = extract_docs(tmp_file)
#             elif file_extension == "pdf":
#                 data = extract_pdf(tmp_file)
#             elif file_extension in ["xlsx", "xls"]:
#                 data = extract_xlsx(tmp_file)
#             else:
#                 return JsonResponse(
#                     {"success": False, "message": "Formato de archivo no soportado."}
#                 )

#             save_entities(data)
#             return JsonResponse({"success": True})
#         except Exception as e:
#             return JsonResponse({"success": False, "message": str(e)})
#         finally:
#             default_storage.delete(tmp_file)

#     return JsonResponse(
#         {"success": False, "message": "No se ha subido ningún archivo."}
#     )


def PredecirDesercion(request):
    params = params_list[0]

    y0 = [500, 0, 0, 0]

    t_span = [0, 180]
    t_eval = np.linspace(t_span[0], t_span[1], 1000)

    sol = solve_ivp(
        model,
        t_span,
        y0,
        t_eval=t_eval,
        args=(
            params["ciclo"],
            params["for"],
            params["trab"],
            params["disc"],
            params["edu"],
            params["hijos"],
            params["gen"],
        ),
    )

    S_sol = sol.y[0]
    R_sol = sol.y[1]
    D_sol = sol.y[2]
    A_sol = sol.y[3]

    prob_desercion = np.clip((D_sol / 500) * 100, 1, 100)

    prob_desercion_final = prob_desercion[-1]

    plt.figure(figsize=(10, 6))
    plt.plot(sol.t, S_sol, label="Estudiantes Matriculados (S(t))")
    plt.plot(sol.t, R_sol, label="Estudiantes Reprobados (R(t))")
    plt.plot(sol.t, D_sol, label="Estudiantes Desertores (D(t))")
    plt.plot(sol.t, A_sol, label="Estudiantes Aprobados (A(t))")
    plt.xlabel("Tiempo (días)")
    plt.ylabel("Número de estudiantes")
    plt.title(
        f'Parámetros para Género {params["gen"]}: Ciclo {params["ciclo"]}, Foráneo {params["for"]}, Trabaja {params["trab"]}, Discapacidad {params["disc"]}, Educación {params["edu"]}, Hijos {params["hijos"]}'
    )
    plt.legend()
    plt.grid()

    plt.figure(figsize=(10, 6))
    plt.plot(sol.t, prob_desercion, label="Probabilidad de Deserción (%)")
    plt.xlabel("Tiempo (días)")
    plt.ylabel("Probabilidad de Deserción (%)")
    plt.title(f'Probabilidad de Deserción para Género {params["gen"]}')
    plt.legend()
    plt.grid()
    plt.ylim(1, 100)

    plt.tight_layout()

    filename = os.path.join(
        settings.STATIC_ROOT,
        "Predicciones",
        "prediccion.png",
    )

    try:
        plt.savefig(filename)
        plt.close()

    except Exception as e:
        print(f"Error al guardar la imagen: {e}")

    relative_filename = os.path.join(
        settings.STATIC_URL,
        "Predicciones",
        "prediccion.png",
    )

    return render(
        request,
        "PredecirDesercion.html",
        {"prediccion": prob_desercion_final, "imagen": relative_filename},
    )


# def PredecirDesercion(request):
#     params = params_list[0]

#     y0 = [500, 0, 0, 0]

#     t_span = [0, 180]
#     t_eval = np.linspace(t_span[0], t_span[1], 1000)

#     sol = solve_ivp(
#         model,
#         t_span,
#         y0,
#         t_eval=t_eval,
#         args=(
#             params["ciclo"],
#             params["for"],
#             params["trab"],
#             params["disc"],
#             params["edu"],
#             params["hijos"],
#             params["gen"],
#         ),
#     )

#     S_sol = sol.y[0]
#     R_sol = sol.y[1]
#     D_sol = sol.y[2]
#     A_sol = sol.y[3]

#     prob_desercion = np.clip((D_sol / 500) * 100, 1, 100)

#     prob_desercion_final = prob_desercion[-1]

#     plt.figure(figsize=(10, 6))
#     plt.plot(sol.t, S_sol, label="Estudiantes Matriculados (S(t))")
#     plt.plot(sol.t, R_sol, label="Estudiantes Reprobados (R(t))")
#     plt.plot(sol.t, D_sol, label="Estudiantes Desertores (D(t))")
#     plt.plot(sol.t, A_sol, label="Estudiantes Aprobados (A(t))")
#     plt.xlabel("Tiempo (días)")
#     plt.ylabel("Número de estudiantes")
#     plt.title(
#         f'Parámetros para Género {params["gen"]}: Ciclo {params["ciclo"]}, Foráneo {params["for"]}, Trabaja {params["trab"]}, Discapacidad {params["disc"]}, Educación {params["edu"]}, Hijos {params["hijos"]}'
#     )
#     plt.legend()
#     plt.grid()

#     plt.figure(figsize=(10, 6))
#     plt.plot(sol.t, prob_desercion, label="Probabilidad de Deserción (%)")
#     plt.xlabel("Tiempo (días)")
#     plt.ylabel("Probabilidad de Deserción (%)")
#     plt.title(f'Probabilidad de Deserción para Género {params["gen"]}')
#     plt.legend()
#     plt.grid()
#     plt.ylim(1, 100)

#     plt.tight_layout()
#     filename = os.path.join(
#         "C:\\Users\\Victor\\Documents\\Proyectos 4 ciclo\\PIS-CUARTO_CICLO\\PIS\\Static\\Predicciones",
#         "prediccion.png",
#     )
#     plt.savefig(filename)
#     plt.close()
#     # plt.savefig("../Static/Predicciones/prediccion.png")

#     return render(
#         request, "PredecirDesercion.html", {"prediccion": prob_desercion_final}
#     )
