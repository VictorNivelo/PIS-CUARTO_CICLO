from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .Modelo.ModeloMatematico import model, params_list
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from datetime import datetime, timedelta
from django.db.models import Avg, StdDev
from PIS.decorators import require_role
from django.core.mail import send_mail
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from scipy.integrate import odeint
from django.db import transaction
from django.conf import settings
from django.db.models import Avg
import matplotlib.pyplot as plt
from django.urls import reverse
from django.db.models import Q
from django.views import View
from scipy.stats import norm
from docx import Document
import numpy as np
import pdfplumber
import openpyxl
import logging
import PyPDF2
import json
import csv
import re
import os
from PIS.models import (
    Usuario,
    PeriodoAcademico,
    DatosHistorico,
    Universidad,
    Estudiante,
    Facultad,
    Carrera,
    Materia,
    TipoDNI,
    Genero,
    Ciclo,
)
from .forms import (
    RecuperarContraseniaForm,
    RegistrarEstudianteForm,
    CambiarContraseniaForm,
    RegistrarUsuarioForm,
    PeriodoAcademicoForm,
    DatosHistoricosForm,
    InicioSesionForm,
    UniversidadForm,
    FacultadForm,
    CarreraForm,
    MateriaForm,
    TipoDNIForm,
    GeneroForm,
    CicloForm,
)


def PaginaAyuda(request):
    return render(request, "PaginaAyuda.html")


def PaginaPrincipal(request):
    return render(request, "Index.html")


@login_required
def PaginaAdministrador(request):
    return render(request, "PaginaAdministrador.html")


@login_required
def PaginaDocente(request):
    user = request.user
    materias = Materia.objects.filter(docente_encargado=user)

    context = {
        "user": user,
        "materias": materias,
    }

    return render(request, "PaginaDocente.html", context)


@login_required
def PaginaSecretaria(request):
    return render(request, "PaginaSecretaria.html")


def sin_acceso(request):
    return render(request, "sin_acceso.html")


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


# funciones de usuario


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


def CorreoEnviado(request, uidb64, token):
    return render(request, "CorreoRecuperacionEnviado.html")


User = get_user_model()


def RecuperarContrasenia(request):
    if request.method == "POST":
        form = RecuperarContraseniaForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data["username"]
            try:
                user = Usuario.objects.get(username=username_or_email)
            except User.DoesNotExist:
                try:
                    user = Usuario.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    messages.error(
                        request, "El usuario o correo electrónico no existe."
                    )
                    return render(request, "RecuperarContrasenia.html", {"form": form})

            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = request.build_absolute_uri(
                reverse(
                    "Cambiar_Contrasenia", kwargs={"uidb64": uidb64, "token": token}
                )
            )

            subject = "Recuperación de contraseña"
            message = f"""
            Hola {user.username},

            Has solicitado restablecer tu contraseña. Sigue estos pasos:

            1. Haz clic en el siguiente enlace: {reset_url}
            2. Se te dirigirá a una página donde podrás ingresar tu nueva contraseña.
            3. Ingresa tu nueva contraseña y confírmala.
            4. Haz clic en "Cambiar".

            Si no solicitaste este cambio, ignora este correo.

            Saludos,
            El equipo de soporte
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Se ha enviado un correo con instrucciones para recuperar tu contraseña.",
            )
            return redirect("Correo_Enviado", uidb64=uidb64, token=token)
            # return redirect("Correo_Enviado")
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


# funciones de personal administrativo


@csrf_exempt
@require_http_methods(["GET", "POST"])
def RegistrarUsuario(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = RegistrarUsuarioForm(data)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                if Usuario.objects.filter(username=user.username).exists():
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Ya existe un usuario con este correo",
                        }
                    )

                if Usuario.objects.filter(dni=user.dni).exists():
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Ya existe Usuario con este DNI.",
                        }
                    )

                num_usuarios = Usuario.objects.count()
                if num_usuarios == 0:
                    user.is_superuser = True
                    user.is_staff = True
                    user.rol = "Personal Administrativo"
                elif num_usuarios == 1:
                    user.is_staff = True
                    user.rol = "Secretaria"
                else:
                    user.rol = "Docente"

                user.set_password(form.cleaned_data["password1"])
                user.save()
                login(request, user)

                return JsonResponse(
                    {"status": "success", "message": "Usuario registrado exitosamente."}
                )

            except Exception as e:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": f"Error al guardar el usuario: {str(e)}",
                    }
                )
        else:
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    if (
                        field == "username"
                        and "Ya existe un usuario con este nombre" in error
                    ):
                        error = "Ya existe un usuario con este correo"
                    errors.append(error)

            return JsonResponse({"status": "error", "errors": errors})
    else:
        form = RegistrarUsuarioForm()

    return render(request, "RU-CrearUsuario.html", {"form": form})


def GestionUsuario(request):
    query = request.GET.get("search_query", "")
    filter_rol = request.GET.get("rol", "")
    filter_genero = request.GET.get("genero", "")
    filter_tipo_dni = request.GET.get("tipo_dni", "")

    usuarios = Usuario.objects.all()
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
            usuario = Usuario.objects.get(id=user_id)
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
                    fecha_nacimiento_str, "%Y-%m-%d"
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
            usuario = Usuario.objects.get(id=user_id)
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
            estudiante.estado = request.POST.get("estado")
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
            facultad.abreviacion = request.POST.get("abreviacion")
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
    periodosAcademicos = PeriodoAcademico.objects.all()

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
            "periodosAcademicos": periodosAcademicos,
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
    periodosAcademicos = PeriodoAcademico.objects.all()
    docentes = Usuario.objects.filter(rol="Docente")

    if query:
        materias = materias.filter(Q(nombre_materia__icontains=query))

    if request.method == "POST":
        if "modify" in request.POST:
            materia_id = request.POST.get("materia_id")
            try:
                materia = Materia.objects.get(id=materia_id)
            except Materia.DoesNotExist:
                messages.error(request, "Materia no encontrada.")
                return redirect("Gestion_Materia")

            materia.nombre_materia = request.POST.get("nombre_materia")
            materia.numero_horas = request.POST.get("numero_horas")
            materia.unidades = request.POST.get("unidades")
            docente_encargado_id = request.POST.get("docente_encargado")
            ciclo_id = request.POST.get("ciclo")

            try:
                docente = Usuario.objects.get(id=docente_encargado_id)
                ciclo = Ciclo.objects.get(id=ciclo_id)

                materia.docente_encargado = docente
                materia.ciclo = ciclo

                materia.save()
                messages.success(request, "Materia actualizada exitosamente.")

            except (
                PeriodoAcademico.DoesNotExist,
                Usuario.DoesNotExist,
                Ciclo.DoesNotExist,
            ):
                messages.error(
                    request, "Error: Uno de los objetos requeridos no existe."
                )

        elif "delete" in request.POST:
            materia_id = request.POST.get("materia_id")
            try:
                materia = Materia.objects.get(id=materia_id)
                materia.delete()
                messages.success(request, "Materia eliminada exitosamente.")
            except Materia.DoesNotExist:
                messages.error(request, "Materia no encontrada.")

        return redirect("Gestion_Materia")

    return render(
        request,
        "GestionMateria.html",
        {
            "materias": materias,
            "docentes": docentes,
            "ciclos": ciclos,
            "periodosAcademicos": periodosAcademicos,
            "query": query,
        },
    )


def RegistrarDatosHistorico(request):
    if request.method == "POST":
        form = DatosHistoricosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos históricos registrados exitosamente.")
            return redirect("Gestion_DatosHistorico")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = DatosHistoricosForm()

    return render(request, "RDH-CrearDatosHistoricos.html", {"form": form})


def GestionDatosHistoricos(request):
    query = request.GET.get("search_query", "")
    datosHistoricos = DatosHistorico.objects.all()
    materias = Materia.objects.all()
    periodosAcademico = PeriodoAcademico.objects.all()

    if query:
        datosHistoricos = datosHistoricos.filter(
            Q(cantidad_matriculados__icontains=query)
        )

    if request.method == "POST":
        if "modify" in request.POST:
            datos_historicos_id = request.POST.get("datosHistoricos_id")
            datos_historicos = DatosHistorico.objects.get(id=datos_historicos_id)

            datos_historicos.materia_id = request.POST.get("materia")
            datos_historicos.periodo_academico_id = request.POST.get(
                "periodo_academico"
            )
            datos_historicos.cantidad_matriculados = int(
                request.POST.get("cantidad_matriculados")
            )
            datos_historicos.cantidad_aprobados = int(
                request.POST.get("cantidad_aprobados")
            )
            datos_historicos.cantidad_reprobados = int(
                request.POST.get("cantidad_reprobados")
            )
            datos_historicos.cantidad_desertores = int(
                request.POST.get("cantidad_desertores")
            )
            datos_historicos.promedio_modalidad = float(
                request.POST.get("promedio_modalidad")
            )
            datos_historicos.promedio_tipo_educacion = float(
                request.POST.get("promedio_tipo_educacion")
            )
            datos_historicos.promedio_origen = float(
                request.POST.get("promedio_origen")
            )
            datos_historicos.promedio_trabajo = float(
                request.POST.get("promedio_trabajo")
            )
            datos_historicos.promedio_discapacidad = float(
                request.POST.get("promedio_discapacidad")
            )
            datos_historicos.promedio_hijos = float(request.POST.get("promedio_hijos"))

            try:
                datos_historicos.save()
                messages.success(request, "Dato histórico actualizado exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al actualizar: {str(e)}")

        elif "delete" in request.POST:
            datos_historicos_id = request.POST.get("datosHistoricos_id")
            datos_historicos = DatosHistorico.objects.get(id=datos_historicos_id)
            datos_historicos.delete()
            messages.success(request, "Dato histórico eliminado exitosamente.")

        return redirect("Gestion_DatosHistorico")

    context = {
        "DatosHistorico": datosHistoricos,
        "periodosAcademico": periodosAcademico,
        "materias": materias,
        "search_query": query,
    }
    return render(request, "GestionDatosHistoricos.html", context)


# importar datos desde csv


def get_or_create_related(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return model.objects.create(**kwargs)


def ImportarDatosCVS(model, csv_file):
    decoded_file = csv_file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded_file)

    created_count = 0
    errors = []

    with transaction.atomic():
        for row in reader:
            try:
                if model == Usuario:
                    genero = get_or_create_related(Genero, nombre_genero=row["genero"])
                    tipo_dni = get_or_create_related(
                        TipoDNI, nombre_tipo_dni=row["tipo_dni"]
                    )
                    instance = Usuario(
                        username=row["username"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        email=row["email"],
                        genero=genero,
                        fecha_nacimiento=row["fecha_nacimiento"],
                        dni=row["dni"],
                        tipo_dni=tipo_dni,
                        telefono=row["telefono"],
                        rol=row["rol"],
                    )
                    instance.set_password(row["password"])

                elif model == Estudiante:
                    tipo_dni = get_or_create_related(
                        TipoDNI, nombre_tipo_dni=row["tipo_dni"]
                    )
                    genero = get_or_create_related(Genero, nombre_genero=row["genero"])
                    instance = Estudiante(
                        tipo_dni=tipo_dni,
                        dni_estudiante=row["dni_estudiante"],
                        nombre_estudiante=row["nombre_estudiante"],
                        apellido_estudiante=row["apellido_estudiante"],
                        genero=genero,
                        modalidad_estudio=int(row["modalidad_estudio"]),
                        tipo_educacion=int(row["tipo_educacion"]),
                        origen=int(row["origen"]),
                        trabajo=int(row["trabajo"]),
                        discapacidad=int(row["discapacidad"]),
                        hijos=int(row["hijos"]),
                        estado=row["estado"],
                    )

                elif model == Genero:
                    instance = Genero(
                        nombre_genero=row["nombre_genero"],
                        descripcion_genero=row["descripcion_genero"],
                    )

                elif model == TipoDNI:
                    instance = TipoDNI(
                        nombre_tipo_dni=row["nombre_tipo_dni"],
                        descripcion_tipo_dni=row["descripcion_tipo_dni"],
                    )

                elif model == Universidad:
                    instance = Universidad(
                        nombre_universidad=row["nombre_universidad"],
                        direccion_universidad=row["direccion_universidad"],
                        telefono_universidad=row["telefono_universidad"],
                        correo_universidad=row["correo_universidad"],
                        fecha_fundacion=row["fecha_fundacion"],
                    )

                elif model == Facultad:
                    universidad = get_or_create_related(
                        Universidad, nombre_universidad=row["universidad"]
                    )
                    instance = Facultad(
                        nombre_facultad=row["nombre_facultad"],
                        fecha_fundacion=row["fecha_fundacion"],
                        universidad=universidad,
                    )

                elif model == Carrera:
                    facultad = get_or_create_related(
                        Facultad, nombre_facultad=row["facultad"]
                    )
                    instance = Carrera(
                        nombre_carrera=row["nombre_carrera"],
                        duracion=int(row["duracion"]),
                        facultad=facultad,
                    )

                elif model == Ciclo:
                    carrera = get_or_create_related(
                        Carrera, nombre_carrera=row["carrera"]
                    )
                    instance = Ciclo(
                        nombre_ciclo=row["nombre_ciclo"],
                        fecha_inicio=row["fecha_inicio"],
                        fecha_fin=row["fecha_fin"],
                        carrera=carrera,
                    )

                elif model == Materia:
                    periodo_academico = get_or_create_related(
                        PeriodoAcademico,
                        codigo_periodo_academico=row["periodo_academico"],
                    )
                    docente = get_or_create_related(
                        Usuario, username=row["docente_encargado"]
                    )
                    ciclo = get_or_create_related(Ciclo, nombre_ciclo=row["ciclo"])
                    instance = Materia(
                        nombre_materia=row["nombre_materia"],
                        numero_horas=int(row["numero_horas"]),
                        unidades=int(row["unidades"]) if row["unidades"] else None,
                        periodo_academico=periodo_academico,
                        docente_encargado=docente,
                        ciclo=ciclo,
                    )

                elif model == PeriodoAcademico:
                    instance = PeriodoAcademico(
                        codigo_periodo_academico=row["codigo_periodo_academico"],
                        fecha_inicio=row["fecha_inicio"],
                        fecha_fin=row["fecha_fin"],
                        estado_periodo_academico=row["estado_periodo_academico"],
                    )

                elif model == DatosHistorico:
                    materia = get_or_create_related(
                        Materia, nombre_materia=row["materia"]
                    )
                    instance = DatosHistorico(
                        materia=materia,
                        cantidad_matriculados=int(row["cantidad_matriculados"]),
                        cantidad_aprobados=int(row["cantidad_aprobados"]),
                        cantidad_reprobados=int(row["cantidad_reprobados"]),
                        cantidad_desertores=int(row["cantidad_desertores"]),
                    )

                else:
                    raise ValueError(f"Modelo no soportado: {model.__name__}")

                instance.full_clean()
                instance.save()

                if model == Estudiante:
                    for materia_nombre in row["materias"].split(","):
                        materia = get_or_create_related(
                            Materia, nombre_materia=materia_nombre.strip()
                        )
                        instance.materia.add(materia)

                created_count += 1

            except Exception as e:
                errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

    return created_count, errors


def ImportarDatosModelo(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        model_name = request.POST.get("model_name")

        if not csv_file:
            messages.error(request, "Por favor, seleccione un archivo CSV.")
            return redirect("Importar_Datos")

        if not model_name:
            messages.error(request, "Por favor, seleccione un modelo.")
            return redirect("Importar_Datos")

        model_map = {
            "usuario": Usuario,
            "estudiante": Estudiante,
            "genero": Genero,
            "tipoDNI": TipoDNI,
            "universidad": Universidad,
            "facultad": Facultad,
            "carrera": Carrera,
            "ciclo": Ciclo,
            "materia": Materia,
            "periodoAcademico": PeriodoAcademico,
        }

        model = model_map.get(model_name.lower())
        if not model:
            messages.error(request, "Modelo no válido seleccionado.")
            return redirect("Importar_Datos")

        try:
            created_count, errors = ImportarDatosCVS(model, csv_file)
            if errors:
                for error in errors:
                    messages.warning(request, error)
            messages.success(
                request, f"Se importaron exitosamente {created_count} registros."
            )
        except Exception as e:
            messages.error(request, f"Error durante la importación: {str(e)}")

        return redirect("Importar_Datos")

    return render(request, "ImportarDatos.html")


# Importar informacion por entidad


@csrf_exempt
def ImportarUsuario(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    genero = get_or_create_related(Genero, nombre_genero=row["genero"])
                    tipo_dni = get_or_create_related(
                        TipoDNI, nombre_tipo_dni=row["tipo_dni"]
                    )
                    instance = Usuario(
                        username=row["username"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        email=row["email"],
                        genero=genero,
                        fecha_nacimiento=row["fecha_nacimiento"],
                        tipo_dni=tipo_dni,
                        dni=row["dni"],
                        telefono=row["telefono"],
                        rol=row["rol"],
                    )
                    instance.set_password(row["password"])

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} usuarios, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} usuarios.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarEstudiante(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    tipo_dni = get_or_create_related(
                        TipoDNI, nombre_tipo_dni=row["tipo_dni"]
                    )
                    genero = get_or_create_related(Genero, nombre_genero=row["genero"])
                    instance = Estudiante(
                        tipo_dni=tipo_dni,
                        dni_estudiante=row["dni_estudiante"],
                        nombre_estudiante=row["nombre_estudiante"],
                        apellido_estudiante=row["apellido_estudiante"],
                        genero=genero,
                        modalidad_estudio=int(row["modalidad_estudio"]),
                        tipo_educacion=int(row["tipo_educacion"]),
                        origen=int(row["origen"]),
                        trabajo=int(row["trabajo"]),
                        discapacidad=int(row["discapacidad"]),
                        hijos=int(row["hijos"]),
                        estado=row["estado"],
                    )

                    instance.full_clean()
                    instance.save()
                    for materia_nombre in row["materias"].split(","):
                        materia = get_or_create_related(
                            Materia, nombre_materia=materia_nombre.strip()
                        )
                        instance.materia.add(materia)

                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} estudiantes, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} estudiantes.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarGenero(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    instance = Genero(
                        nombre_genero=row["nombre_genero"],
                        descripcion_genero=row["descripcion_genero"],
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} generos, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} generos.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarTipoDNI(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    instance = TipoDNI(
                        nombre_tipo_dni=row["nombre_tipo_dni"],
                        descripcion_tipo_dni=row["descripcion_tipo_dni"],
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} tipos de DNI, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} tipos de DNI.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarUniversidades(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    instance = Universidad(
                        nombre_universidad=row["nombre_universidad"],
                        direccion_universidad=row["direccion_universidad"],
                        telefono_universidad=row["telefono_universidad"],
                        correo_universidad=row["correo_universidad"],
                        fecha_fundacion=row["fecha_fundacion"],
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} universidades, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} universidades.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarFacultades(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    universidad = get_or_create_related(
                        Universidad, nombre_universidad=row["universidad"]
                    )
                    instance = Facultad(
                        nombre_facultad=row["nombre_facultad"],
                        abreviacion=row["abreviacion"],
                        fecha_fundacion=row["fecha_fundacion"],
                        universidad=universidad,
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} facultades, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} facultades.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarCarreras(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    facultad = get_or_create_related(
                        Facultad, nombre_facultad=row["facultad"]
                    )
                    instance = Carrera(
                        nombre_carrera=row["nombre_carrera"],
                        duracion=int(row["duracion"]),
                        facultad=facultad,
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} carreras, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} carreras.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarCiclos(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    carrera = get_or_create_related(
                        Carrera, nombre_carrera=row["carrera"]
                    )
                    periodo_academico = get_or_create_related(
                        PeriodoAcademico,
                        codigo_periodo_academico=row["periodo_academico"],
                    )
                    instance = Ciclo(
                        nombre_ciclo=row["nombre_ciclo"],
                        numero_ciclo=row["numero_ciclo"],
                        periodo_academico=periodo_academico,
                        carrera=carrera,
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} ciclos, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} ciclos.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarMaterias(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    docente = get_or_create_related(
                        Usuario, username=row["docente_encargado"]
                    )
                    ciclo = get_or_create_related(Ciclo, nombre_ciclo=row["ciclo"])
                    instance = Materia(
                        nombre_materia=row["nombre_materia"],
                        numero_horas=int(row["numero_horas"]),
                        unidades=int(row["unidades"]) if row["unidades"] else None,
                        docente_encargado=docente,
                        ciclo=ciclo,
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} materias, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} materias.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarPeriodoAcademicos(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    instance = PeriodoAcademico(
                        codigo_periodo_academico=row["codigo_periodo_academico"],
                        fecha_inicio=row["fecha_inicio"],
                        fecha_fin=row["fecha_fin"],
                        estado_periodo_academico=row["estado_periodo_academico"],
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} periodos academicos, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} periodos academicos.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


@csrf_exempt
def ImportarDatoHistoricos(request):
    if request.method != "POST" or not request.FILES.get("document"):
        return JsonResponse(
            {
                "success": False,
                "errors": ["Método no permitido o archivo no proporcionado"],
            }
        )

    csv_file = request.FILES["document"]

    try:
        decoded_file = csv_file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created_count = 0
        errors = []

        with transaction.atomic():
            for row in reader:
                try:
                    materia = get_or_create_related(
                        Materia, nombre_materia=row["materia"]
                    )
                    periodo_academico = get_or_create_related(
                        PeriodoAcademico,
                        codigo_periodo_academico=row["periodo_academico"],
                    )
                    instance = DatosHistorico(
                        materia=materia,
                        periodo_academico=periodo_academico,
                        cantidad_matriculados=int(row["cantidad_matriculados"]),
                        cantidad_aprobados=int(row["cantidad_aprobados"]),
                        cantidad_reprobados=int(row["cantidad_reprobados"]),
                        cantidad_desertores=int(row["cantidad_desertores"]),
                        promedio_modalidad=float(row["promedio_modalidad"]),
                        promedio_tipo_educacion=float(row["promedio_tipo_educacion"]),
                        promedio_origen=float(row["promedio_origen"]),
                        promedio_trabajo=float(row["promedio_trabajo"]),
                        promedio_discapacidad=float(row["promedio_discapacidad"]),
                        promedio_hijos=float(row["promedio_hijos"]),
                    )

                    instance.full_clean()
                    instance.save()
                    created_count += 1

                except Exception as e:
                    errors.append(f"Error en la fila {reader.line_num}: {str(e)}")

        if errors:
            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                    "message": f"Se importaron {created_count} datos históricos, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} datos históricos.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})


# Obtencion de los datos para la prediccion


def ObtenerUniversidades(request):
    universidades = Universidad.objects.all().values("id", "nombre_universidad")
    return JsonResponse(list(universidades), safe=False)


def ObtenerFacultades(request):
    facultades = Facultad.objects.all().values("id", "abreviacion")
    return JsonResponse(list(facultades), safe=False)


def ObtenerCarreras(request):
    facultad_id = request.GET.get("facultad_id")
    carreras = Carrera.objects.filter(facultad_id=facultad_id).values(
        "id", "nombre_carrera"
    )
    return JsonResponse(list(carreras), safe=False)


def ObtenerCiclos(request):
    carrera_id = request.GET.get("carrera_id")
    ciclos = Ciclo.objects.filter(carrera_id=carrera_id).values("id", "nombre_ciclo")
    return JsonResponse(list(ciclos), safe=False)


def ObtenerMaterias(request):
    ciclo_id = request.GET.get("ciclo_id")
    materias = Materia.objects.filter(ciclo_id=ciclo_id).values("id", "nombre_materia")
    return JsonResponse(list(materias), safe=False)


def ObtenerDocentes(request):
    materia_id = request.GET.get("materia_id")
    try:
        materia = Materia.objects.get(id=materia_id)
        docente = materia.docente_encargado
        return JsonResponse(
            {"nombre_docente": f"{docente.first_name} {docente.last_name}"}
        )
    except Materia.DoesNotExist:
        return JsonResponse({"nombre_docente": "No asignado"}, status=404)


def monte_carlo(valores_iniciales, num_simulaciones, num_anios):
    resultados = np.zeros((num_simulaciones, len(valores_iniciales), num_anios))
    for sim in range(num_simulaciones):
        for metrica in range(len(valores_iniciales)):
            resultados[sim, metrica, 0] = valores_iniciales[metrica]
            for anio in range(1, num_anios):
                resultados[sim, metrica, anio] = resultados[sim, metrica, anio - 1] * (
                    1 + np.random.normal(0.05, 0.1)
                )
    return np.mean(resultados, axis=0)


logger = logging.getLogger(__name__)


def RungeKutta(f, y0, t, args=()):
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    for i in range(n - 1):
        h = t[i + 1] - t[i]
        k1 = np.array(f(y[i], t[i], *args))
        k2 = np.array(f(y[i] + k1 * h / 2.0, t[i] + h / 2.0, *args))
        k3 = np.array(f(y[i] + k2 * h / 2.0, t[i] + h / 2.0, *args))
        k4 = np.array(f(y[i] + k3 * h, t[i] + h, *args))
        y[i + 1] = y[i] + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


def SistemaEcuaciones(y, t, params):
    M, A, R, D, Mo, Te, O, Tr, Di, H = y
    a, b, c, d, e, f, g, h, i, j = params
    dMdt = a * M * (1 - M / 100) - b * M
    dAdt = c * M - d * A
    dRdt = e * M - f * R
    dDdt = g * M - h * D
    dModt = i * (Mo - Mo**2 / 100)
    dTedt = j * (Te - Te**2 / 100)
    dOdt = i * (O - O**2 / 100)
    dTrdt = j * (Tr - Tr**2 / 100)
    dDidt = i * (Di - Di**2 / 100)
    dHdt = j * (H - H**2 / 100)
    return [dMdt, dAdt, dRdt, dDdt, dModt, dTedt, dOdt, dTrdt, dDidt, dHdt]


def RealizarPrediccion(request):
    if request.method == "POST":
        materia_id = request.POST.get("materia")
        anio_inicio = int(request.POST.get("anio_inicio"))
        anio_fin = int(request.POST.get("anio_fin"))

        try:
            datos_historicos = DatosHistorico.objects.filter(
                materia_id=materia_id
            ).order_by("periodo_academico__fecha_inicio")

            datos_historicos_lista = list(
                datos_historicos.values(
                    "periodo_academico__fecha_inicio__year",
                    "periodo_academico__codigo_periodo_academico",
                    "cantidad_matriculados",
                    "cantidad_aprobados",
                    "cantidad_reprobados",
                    "cantidad_desertores",
                    "promedio_modalidad",
                    "promedio_tipo_educacion",
                    "promedio_origen",
                    "promedio_trabajo",
                    "promedio_discapacidad",
                    "promedio_hijos",
                )
            )

            stats = datos_historicos.aggregate(
                Avg("cantidad_matriculados"),
                Avg("cantidad_aprobados"),
                Avg("cantidad_reprobados"),
                Avg("cantidad_desertores"),
                Avg("promedio_modalidad"),
                Avg("promedio_tipo_educacion"),
                Avg("promedio_origen"),
                Avg("promedio_trabajo"),
                Avg("promedio_discapacidad"),
                Avg("promedio_hijos"),
            )

            params = [0.2, 0.1, 0.6, 0.2, 0.3, 0.1, 0.2, 0.1, 0.05, 0.05]

            y0 = np.array(
                [
                    stats["cantidad_matriculados__avg"] or 0,
                    stats["cantidad_aprobados__avg"] or 0,
                    stats["cantidad_reprobados__avg"] or 0,
                    stats["cantidad_desertores__avg"] or 0,
                    stats["promedio_modalidad__avg"] or 0,
                    stats["promedio_tipo_educacion__avg"] or 0,
                    stats["promedio_origen__avg"] or 0,
                    stats["promedio_trabajo__avg"] or 0,
                    stats["promedio_discapacidad__avg"] or 0,
                    stats["promedio_hijos__avg"] or 0,
                ]
            )

            t = np.linspace(
                0, anio_fin - anio_inicio + 1, (anio_fin - anio_inicio + 1) * 2
            )

            sol = RungeKutta(SistemaEcuaciones, y0, t, args=(params,))

            ruido = np.random.normal(0, 0.02, sol.shape)
            sol_con_ruido = sol + ruido * sol

            sol_con_ruido = np.clip(sol_con_ruido, 0, 100)

            for i in range(len(sol_con_ruido)):
                total = sol_con_ruido[i, 1] + sol_con_ruido[i, 2] + sol_con_ruido[i, 3]
                if total > sol_con_ruido[i, 0]:
                    factor = sol_con_ruido[i, 0] / total
                    sol_con_ruido[i, 1:4] *= factor

            años = list(range(anio_inicio, anio_fin + 1))
            periodos = []
            for año in años:
                periodos.extend([f"{año}-1", f"{año}-2"])

            predicciones = {
                "años": años,
                "periodos": periodos,
                "matriculados": sol_con_ruido[:, 0].tolist(),
                "aprobados": sol_con_ruido[:, 1].tolist(),
                "reprobados": sol_con_ruido[:, 2].tolist(),
                "desertores": sol_con_ruido[:, 3].tolist(),
                "modalidad": sol_con_ruido[:, 4].tolist(),
                "tipo_educacion": sol_con_ruido[:, 5].tolist(),
                "origen": sol_con_ruido[:, 6].tolist(),
                "trabajo": sol_con_ruido[:, 7].tolist(),
                "discapacidad": sol_con_ruido[:, 8].tolist(),
                "hijos": sol_con_ruido[:, 9].tolist(),
                "datosHistoricos": datos_historicos_lista,
            }

            return JsonResponse(predicciones)

        except Exception as e:
            logger.error(f"Error en RealizarPrediccion: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def PrediccionMateria(request):
    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()
    ciclos = Ciclo.objects.all()
    materias = Materia.objects.all()
    datosHistoricos = DatosHistorico.objects.all()

    context = {
        "facultades": facultades,
        "carreras": carreras,
        "ciclos": ciclos,
        "materias": materias,
        "datosHistoricos": datosHistoricos,
    }

    return render(request, "PrediccionMateria.html", context)


def RealizarPrediccionCiclo(request):
    if request.method == "POST":
        ciclo_id = request.POST.get("ciclo")
        anio_inicio = int(request.POST.get("anio_inicio"))
        anio_fin = int(request.POST.get("anio_fin"))

        try:
            materias = Materia.objects.filter(ciclo_id=ciclo_id)
            datos_historicos = DatosHistorico.objects.filter(
                materia__in=materias,
                periodo_academico__fecha_inicio__year__gte=anio_inicio,
            ).order_by("periodo_academico__fecha_inicio")

            datos_agrupados = {}
            for dato in datos_historicos:
                año = dato.periodo_academico.fecha_inicio.year
                periodo = f"{año}_{dato.periodo_academico.codigo_periodo_academico}"
                if periodo not in datos_agrupados:
                    datos_agrupados[periodo] = {
                        "año": año,
                        "matriculados": 0,
                        "aprobados": 0,
                        "reprobados": 0,
                        "desertores": 0,
                        "modalidad": 0,
                        "tipo_educacion": 0,
                        "origen": 0,
                        "trabajo": 0,
                        "discapacidad": 0,
                        "hijos": 0,
                        "count": 0,
                        "materias": set(),
                    }
                datos_agrupados[periodo]["matriculados"] += dato.cantidad_matriculados
                datos_agrupados[periodo]["aprobados"] += dato.cantidad_aprobados
                datos_agrupados[periodo]["reprobados"] += dato.cantidad_reprobados
                datos_agrupados[periodo]["desertores"] += dato.cantidad_desertores
                datos_agrupados[periodo]["modalidad"] += dato.promedio_modalidad
                datos_agrupados[periodo][
                    "tipo_educacion"
                ] += dato.promedio_tipo_educacion
                datos_agrupados[periodo]["origen"] += dato.promedio_origen
                datos_agrupados[periodo]["trabajo"] += dato.promedio_trabajo
                datos_agrupados[periodo]["discapacidad"] += dato.promedio_discapacidad
                datos_agrupados[periodo]["hijos"] += dato.promedio_hijos
                datos_agrupados[periodo]["count"] += 1
                datos_agrupados[periodo]["materias"].add(dato.materia.nombre_materia)

            for periodo in datos_agrupados:
                count = datos_agrupados[periodo]["count"]
                for key in [
                    "modalidad",
                    "tipo_educacion",
                    "origen",
                    "trabajo",
                    "discapacidad",
                    "hijos",
                ]:
                    datos_agrupados[periodo][key] = min(
                        datos_agrupados[periodo][key] / count, 100
                    )
                datos_agrupados[periodo]["materias"] = list(
                    datos_agrupados[periodo]["materias"]
                )

            periodos = sorted(datos_agrupados.keys())
            if periodos:
                y0 = np.array(
                    [
                        datos_agrupados[periodos[-1]]["matriculados"],
                        datos_agrupados[periodos[-1]]["aprobados"],
                        datos_agrupados[periodos[-1]]["reprobados"],
                        datos_agrupados[periodos[-1]]["desertores"],
                        datos_agrupados[periodos[-1]]["modalidad"],
                        datos_agrupados[periodos[-1]]["tipo_educacion"],
                        datos_agrupados[periodos[-1]]["origen"],
                        datos_agrupados[periodos[-1]]["trabajo"],
                        datos_agrupados[periodos[-1]]["discapacidad"],
                        datos_agrupados[periodos[-1]]["hijos"],
                    ]
                )
            else:
                y0 = np.array([200, 160, 20, 20, 50, 50, 50, 50, 5, 5])

            params = [0.2, 0.1, 0.6, 0.2, 0.3, 0.1, 0.2, 0.1, 0.05, 0.05]
            t = np.linspace(
                0, anio_fin - anio_inicio + 1, (anio_fin - anio_inicio + 1) * 2
            )
            sol = RungeKutta(SistemaEcuaciones, y0, t, args=(params,))

            ruido = np.random.normal(0, 0.02, sol.shape)
            sol_con_ruido = sol + ruido * sol
            sol_con_ruido = np.clip(sol_con_ruido, 0, 100)

            for i in range(len(sol_con_ruido)):
                total = sol_con_ruido[i, 1] + sol_con_ruido[i, 2] + sol_con_ruido[i, 3]
                if total > sol_con_ruido[i, 0]:
                    factor = sol_con_ruido[i, 0] / total
                    sol_con_ruido[i, 1:4] *= factor

            años = list(range(anio_inicio, anio_fin + 1))
            periodos_prediccion = []
            for año in años:
                periodos_prediccion.extend([f"{año}_Marzo", f"{año}_Septiembre"])

            datos_historicos_formateados = []
            for periodo, datos in datos_agrupados.items():
                datos_historicos_formateados.append(
                    {
                        "periodo_academico": periodo,
                        "año": datos["año"],
                        "materias": datos["materias"],
                        "matriculados": datos["matriculados"],
                        "aprobados": datos["aprobados"],
                        "reprobados": datos["reprobados"],
                        "desertores": datos["desertores"],
                    }
                )

            predicciones = {
                "años": años,
                "periodos": periodos_prediccion,
                "matriculados": sol_con_ruido[:, 0].tolist(),
                "aprobados": sol_con_ruido[:, 1].tolist(),
                "reprobados": sol_con_ruido[:, 2].tolist(),
                "desertores": sol_con_ruido[:, 3].tolist(),
                "modalidad": sol_con_ruido[:, 4].tolist(),
                "tipo_educacion": sol_con_ruido[:, 5].tolist(),
                "origen": sol_con_ruido[:, 6].tolist(),
                "trabajo": sol_con_ruido[:, 7].tolist(),
                "discapacidad": sol_con_ruido[:, 8].tolist(),
                "hijos": sol_con_ruido[:, 9].tolist(),
                "datosHistoricos": datos_historicos_formateados,
                "materias": list(
                    set(
                        materia
                        for periodo in datos_agrupados.values()
                        for materia in periodo["materias"]
                    )
                ),
            }

            return JsonResponse(predicciones)

        except Exception as e:
            logger.error(f"Error en RealizarPrediccionCiclo: {str(e)}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def PrediccionCiclo(request):
    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()
    ciclos = Ciclo.objects.all()
    datosHistoricos = DatosHistorico.objects.all()

    context = {
        "facultades": facultades,
        "carreras": carreras,
        "ciclos": ciclos,
        "datosHistoricos": datosHistoricos,
    }

    return render(request, "PrediccionCiclo.html", context)


def RealizarPrediccionCarrera(request):
    if request.method == "POST":
        carrera_id = request.POST.get("carrera")
        anio_inicio = int(request.POST.get("anio_inicio"))
        anio_fin = int(request.POST.get("anio_fin"))

        try:
            datos_historicos = DatosHistorico.objects.filter(
                materia__ciclo__carrera_id=carrera_id
            ).order_by("periodo_academico__fecha_inicio")

            datos_historicos_lista = list(
                datos_historicos.values(
                    "periodo_academico__fecha_inicio__year",
                    "periodo_academico__codigo_periodo_academico",
                    "cantidad_matriculados",
                    "cantidad_aprobados",
                    "cantidad_reprobados",
                    "cantidad_desertores",
                    "promedio_modalidad",
                    "promedio_tipo_educacion",
                    "promedio_origen",
                    "promedio_trabajo",
                    "promedio_discapacidad",
                    "promedio_hijos",
                )
            )

            stats = datos_historicos.aggregate(
                Avg("cantidad_matriculados"),
                Avg("cantidad_aprobados"),
                Avg("cantidad_reprobados"),
                Avg("cantidad_desertores"),
                Avg("promedio_modalidad"),
                Avg("promedio_tipo_educacion"),
                Avg("promedio_origen"),
                Avg("promedio_trabajo"),
                Avg("promedio_discapacidad"),
                Avg("promedio_hijos"),
            )

            params = [0.2, 0.1, 0.6, 0.2, 0.3, 0.1, 0.2, 0.1, 0.05, 0.05]

            y0 = np.array(
                [
                    stats["cantidad_matriculados__avg"] or 0,
                    stats["cantidad_aprobados__avg"] or 0,
                    stats["cantidad_reprobados__avg"] or 0,
                    stats["cantidad_desertores__avg"] or 0,
                    stats["promedio_modalidad__avg"] or 0,
                    stats["promedio_tipo_educacion__avg"] or 0,
                    stats["promedio_origen__avg"] or 0,
                    stats["promedio_trabajo__avg"] or 0,
                    stats["promedio_discapacidad__avg"] or 0,
                    stats["promedio_hijos__avg"] or 0,
                ]
            )

            t = np.linspace(
                0, anio_fin - anio_inicio + 1, (anio_fin - anio_inicio + 1) * 2
            )

            sol = RungeKutta(SistemaEcuaciones, y0, t, args=(params,))

            ruido = np.random.normal(0, 0.02, sol.shape)
            sol_con_ruido = sol + ruido * sol

            sol_con_ruido = np.clip(sol_con_ruido, 0, 100)

            for i in range(len(sol_con_ruido)):
                total = sol_con_ruido[i, 1] + sol_con_ruido[i, 2] + sol_con_ruido[i, 3]
                if total > sol_con_ruido[i, 0]:
                    factor = sol_con_ruido[i, 0] / total
                    sol_con_ruido[i, 1:4] *= factor

            años = list(range(anio_inicio, anio_fin + 1))
            periodos = []
            for año in años:
                periodos.extend([f"{año}-1", f"{año}-2"])

            predicciones = {
                "años": años,
                "periodos": periodos,
                "matriculados": sol_con_ruido[:, 0].tolist(),
                "aprobados": sol_con_ruido[:, 1].tolist(),
                "reprobados": sol_con_ruido[:, 2].tolist(),
                "desertores": sol_con_ruido[:, 3].tolist(),
                "modalidad": sol_con_ruido[:, 4].tolist(),
                "tipo_educacion": sol_con_ruido[:, 5].tolist(),
                "origen": sol_con_ruido[:, 6].tolist(),
                "trabajo": sol_con_ruido[:, 7].tolist(),
                "discapacidad": sol_con_ruido[:, 8].tolist(),
                "hijos": sol_con_ruido[:, 9].tolist(),
                "datosHistoricos": datos_historicos_lista,
            }

            return JsonResponse(predicciones)

        except Exception as e:
            logger.error(
                f"Error en RealizarPrediccionPorCarrera: {str(e)}", exc_info=True
            )
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def PrediccionCarrera(request):
    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()
    datosHistoricos = DatosHistorico.objects.all()

    context = {
        "facultades": facultades,
        "carreras": carreras,
        "datosHistoricos": datosHistoricos,
    }

    return render(request, "PrediccionCarrera.html", context)


def PRI(request):
    return render(request, "ZZ.html")
