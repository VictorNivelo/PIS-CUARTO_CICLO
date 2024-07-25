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
            materia = Materia.objects.get(id=materia_id)
            materia.nombre_materia = request.POST.get("nombre_materia")
            materia.numero_horas = request.POST.get("numero_horas")
            materia.unidades = request.POST.get("unidades")

            periodo_academico_id = request.POST.get("periodo_academico")
            docente_encargado_id = request.POST.get("docente_encargado")
            ciclo_id = request.POST.get("ciclo")

            try:
                periodo = PeriodoAcademico.objects.get(id=periodo_academico_id)
                docente = Usuario.objects.get(id=docente_encargado_id)
                ciclo = Ciclo.objects.get(id=ciclo_id)

                materia.periodo_academico = periodo
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
            datos_historicos.cantidad_matriculados = request.POST.get(
                "cantidad_matriculados"
            )
            datos_historicos.cantidad_aprobados = request.POST.get("cantidad_aprobados")
            datos_historicos.cantidad_reprobados = request.POST.get(
                "cantidad_reprobados"
            )
            datos_historicos.cantidad_desertores = request.POST.get(
                "cantidad_desertores"
            )
            datos_historicos.promedio_modalidad = request.POST.get("promedio_modalidad")
            datos_historicos.promedio_tipo_educacion = request.POST.get(
                "promedio_tipo_educacion"
            )
            datos_historicos.promedio_origen = request.POST.get("promedio_origen")
            datos_historicos.promedio_trabajo = request.POST.get("promedio_trabajo")
            datos_historicos.promedio_discapacidad = request.POST.get(
                "promedio_discapacidad"
            )
            datos_historicos.promedio_hijos = request.POST.get("promedio_hijos")

            datos_historicos.save()
            messages.success(request, "Dato histórico actualizado exitosamente.")

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


def PredecirMetricas(request):
    if request.method == "POST":
        tipo_prediccion = request.POST.get("tipo_prediccion")
        id_item = request.POST.get("id_item")
        anio_inicio = int(request.POST.get("anio_inicio"))
        anio_fin = int(request.POST.get("anio_fin"))

        filtro_base = {}
        if tipo_prediccion == "facultad":
            filtro_base = {"materia__ciclo__carrera__facultad_id": id_item}
        elif tipo_prediccion == "carrera":
            filtro_base = {"materia__ciclo__carrera_id": id_item}
        elif tipo_prediccion == "ciclo":
            filtro_base = {"materia__ciclo_id": id_item}
        elif tipo_prediccion == "materia":
            filtro_base = {"materia_id": id_item}

        periodos = PeriodoAcademico.objects.filter(
            fecha_inicio__year__gte=anio_inicio, fecha_fin__year__lte=anio_fin
        ).order_by("fecha_inicio")

        datos_historicos = DatosHistorico.objects.filter(**filtro_base)

        promedios_historicos = datos_historicos.aggregate(
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

        metricas_iniciales = [
            promedios_historicos["cantidad_matriculados__avg"],
            promedios_historicos["cantidad_aprobados__avg"],
            promedios_historicos["cantidad_reprobados__avg"],
            promedios_historicos["cantidad_desertores__avg"],
            promedios_historicos["promedio_modalidad__avg"],
            promedios_historicos["promedio_tipo_educacion__avg"],
            promedios_historicos["promedio_origen__avg"],
            promedios_historicos["promedio_trabajo__avg"],
            promedios_historicos["promedio_discapacidad__avg"],
            promedios_historicos["promedio_hijos__avg"],
        ]

        def modelo_crecimiento(tiempo, valores):
            return np.array([0.05 * valor for valor in valores])

        tiempo_simulacion = np.linspace(0, anio_fin - anio_inicio, len(periodos))
        predicciones_rk = runge_kutta(
            modelo_crecimiento, metricas_iniciales, tiempo_simulacion
        )
        predicciones_mc = monte_carlo(metricas_iniciales, 1000, len(periodos))

        resultados_prediccion = {
            "periodos": [p.codigo_periodo_academico for p in periodos],
            "predicciones_rk": predicciones_rk.tolist(),
            "predicciones_mc": predicciones_mc.tolist(),
        }

        return render(
            request, "resultados_prediccion.html", {"resultados": resultados_prediccion}
        )

    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()
    ciclos = Ciclo.objects.all()
    materias = Materia.objects.all()

    return render(
        request,
        "formulario_prediccion.html",
        {
            "facultades": facultades,
            "carreras": carreras,
            "ciclos": ciclos,
            "materias": materias,
        },
    )


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


def runge_kutta(funcion, valores_iniciales, tiempo):
    n = len(tiempo)
    y = np.zeros((n, len(valores_iniciales)))
    y[0] = valores_iniciales
    for i in range(n - 1):
        h = tiempo[i + 1] - tiempo[i]
        k1 = h * funcion(tiempo[i], y[i])
        k2 = h * funcion(tiempo[i] + 0.5 * h, y[i] + 0.5 * k1)
        k3 = h * funcion(tiempo[i] + 0.5 * h, y[i] + 0.5 * k2)
        k4 = h * funcion(tiempo[i] + h, y[i] + k3)
        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return y


import logging

logger = logging.getLogger(__name__)


def RealizarPrediccion(request):
    if request.method == "POST":
        materia_id = request.POST.get("materia")
        anio_inicio = int(request.POST.get("anio_inicio"))
        anio_fin = int(request.POST.get("anio_fin"))

        try:
            materia = Materia.objects.get(id=materia_id)
            datos_historicos = DatosHistorico.objects.filter(
                materia_id=materia_id,
                periodo_academico__fecha_inicio__year__lt=anio_inicio,
            ).order_by("periodo_academico__fecha_inicio")

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
                StdDev("cantidad_matriculados"),
                StdDev("cantidad_aprobados"),
                StdDev("cantidad_reprobados"),
                StdDev("cantidad_desertores"),
                StdDev("promedio_modalidad"),
                StdDev("promedio_tipo_educacion"),
                StdDev("promedio_origen"),
                StdDev("promedio_trabajo"),
                StdDev("promedio_discapacidad"),
                StdDev("promedio_hijos"),
            )

            def sistema_ecuaciones(y, t, params):
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

            params = [0.2, 0.1, 0.6, 0.2, 0.3, 0.1, 0.2, 0.1, 0.05, 0.05]

            y0 = [
                stats["cantidad_matriculados__avg"],
                stats["cantidad_aprobados__avg"],
                stats["cantidad_reprobados__avg"],
                stats["cantidad_desertores__avg"],
                stats["promedio_modalidad__avg"],
                stats["promedio_tipo_educacion__avg"],
                stats["promedio_origen__avg"],
                stats["promedio_trabajo__avg"],
                stats["promedio_discapacidad__avg"],
                stats["promedio_hijos__avg"],
            ]

            t = np.linspace(
                0, anio_fin - anio_inicio + 1, (anio_fin - anio_inicio + 1) * 12
            )

            sol = odeint(sistema_ecuaciones, y0, t, args=(params,))

            ruido = np.random.normal(0, 0.02, sol.shape)
            sol_con_ruido = sol + ruido * sol

            sol_con_ruido = np.clip(sol_con_ruido, 0, 100)

            for i in range(len(sol_con_ruido)):
                total = sol_con_ruido[i, 1] + sol_con_ruido[i, 2] + sol_con_ruido[i, 3]
                if total > sol_con_ruido[i, 0]:
                    factor = sol_con_ruido[i, 0] / total
                    sol_con_ruido[i, 1:4] *= factor

            años = list(range(anio_inicio, anio_fin + 1))
            predicciones = {
                "años": años,
                "matriculados": sol_con_ruido[::12, 0].tolist(),
                "aprobados": sol_con_ruido[::12, 1].tolist(),
                "reprobados": sol_con_ruido[::12, 2].tolist(),
                "desertores": sol_con_ruido[::12, 3].tolist(),
                "modalidad": sol_con_ruido[::12, 4].tolist(),
                "tipo_educacion": sol_con_ruido[::12, 5].tolist(),
                "origen": sol_con_ruido[::12, 6].tolist(),
                "trabajo": sol_con_ruido[::12, 7].tolist(),
                "discapacidad": sol_con_ruido[::12, 8].tolist(),
                "hijos": sol_con_ruido[::12, 9].tolist(),
            }

            return JsonResponse(predicciones)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def PrediccionMateria(request):
    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()
    ciclos = Ciclo.objects.all()
    materias = Materia.objects.all()

    context = {
        "facultades": facultades,
        "carreras": carreras,
        "ciclos": ciclos,
        "materias": materias,
    }

    return render(request, "PrediccionMateria.html", context)


# def RealizarPrediccion(request):
#     if request.method == "POST":
#         materia_id = request.POST.get("materia")
#         anio_inicio = int(request.POST.get("anio_inicio"))
#         anio_fin = int(request.POST.get("anio_fin"))

#         logger.info(f"Realizando predicción para materia {materia_id} desde {anio_inicio} hasta {anio_fin}")

#         try:
#             # Obtener la materia
#             materia = Materia.objects.get(id=materia_id)

#             # Obtener todos los datos históricos de la materia antes del año de inicio
#             datos_historicos = DatosHistorico.objects.filter(
#                 materia_id=materia_id,
#                 periodo_academico__fecha_inicio__year__lt=anio_inicio
#             ).order_by('periodo_academico__fecha_inicio')

#             # Calcular promedios
#             promedios = datos_historicos.aggregate(
#                 Avg('cantidad_matriculados'),
#                 Avg('cantidad_aprobados'),
#                 Avg('cantidad_reprobados'),
#                 Avg('cantidad_desertores'),
#                 Avg('promedio_modalidad'),
#                 Avg('promedio_tipo_educacion'),
#                 Avg('promedio_origen'),
#                 Avg('promedio_trabajo'),
#                 Avg('promedio_discapacidad'),
#                 Avg('promedio_hijos'),
#             )

#             # Preparar datos para la predicción
#             años = list(range(anio_inicio, anio_fin + 1))

#             # Función para aplicar crecimiento y limitar entre 0 y 100
#             def aplicar_crecimiento(valor_base, tasa_crecimiento, num_años):
#                 return [min(max(valor_base * (1 + tasa_crecimiento * i), 0), 100) for i in range(num_años)]

#             # Realizar predicciones
#             num_años = len(años)
#             predicciones = {
#                 'años': años,
#                 'matriculados': aplicar_crecimiento(promedios['cantidad_matriculados__avg'] or 0, 0.02, num_años),
#                 'aprobados': aplicar_crecimiento(promedios['cantidad_aprobados__avg'] or 0, 0.01, num_años),
#                 'reprobados': aplicar_crecimiento(promedios['cantidad_reprobados__avg'] or 0, -0.01, num_años),
#                 'desertores': aplicar_crecimiento(promedios['cantidad_desertores__avg'] or 0, -0.02, num_años),
#                 'modalidad': aplicar_crecimiento(promedios['promedio_modalidad__avg'] or 0, 0.005, num_años),
#                 'tipo_educacion': aplicar_crecimiento(promedios['promedio_tipo_educacion__avg'] or 0, 0.005, num_años),
#                 'origen': aplicar_crecimiento(promedios['promedio_origen__avg'] or 0, 0.005, num_años),
#                 'trabajo': aplicar_crecimiento(promedios['promedio_trabajo__avg'] or 0, 0.005, num_años),
#                 'discapacidad': aplicar_crecimiento(promedios['promedio_discapacidad__avg'] or 0, 0.005, num_años),
#                 'hijos': aplicar_crecimiento(promedios['promedio_hijos__avg'] or 0, 0.005, num_años),
#             }

#             # Agregar separaciones por unidades
#             unidades = materia.unidades
#             if unidades and unidades > 0:
#                 separaciones_unidades = np.linspace(0, len(años) - 1, min(unidades + 1, len(años))).astype(int)
#                 predicciones['separaciones_unidades'] = [años[i] for i in separaciones_unidades if i < len(años)]
#             else:
#                 predicciones['separaciones_unidades'] = []

#             # Obtener periodos académicos para los años de predicción
#             periodos_futuros = PeriodoAcademico.objects.filter(
#                 fecha_inicio__year__gte=anio_inicio,
#                 fecha_fin__year__lte=anio_fin
#             ).order_by('fecha_inicio')

#             # Agregar etiquetas de periodos académicos
#             predicciones['etiquetas_periodos'] = [
#                 f"{periodo.fecha_inicio.strftime('%d/%m/%Y')} - {periodo.fecha_fin.strftime('%d/%m/%Y')}"
#                 for periodo in periodos_futuros
#             ]

#             logger.info(f"Predicciones generadas: {predicciones}")

#             return JsonResponse(predicciones)

#         except Exception as e:
#             logger.error(f"Error en RealizarPrediccion: {str(e)}")
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"error": "Método no permitido"}, status=405)

# ================================================================================================

# def RealizarPrediccion(request):
#     if request.method == "POST":
#         facultad_id = request.POST.get("facultad")
#         carrera_id = request.POST.get("carrera")
#         ciclo_id = request.POST.get("ciclo")
#         materia_id = request.POST.get("materia")
#         anio_inicio = int(request.POST.get("anio_inicio"))
#         anio_fin = int(request.POST.get("anio_fin"))

#         datos_historicos = DatosHistorico.objects.filter(
#             materia__ciclo__carrera__facultad_id=facultad_id,
#             materia__ciclo__carrera_id=carrera_id,
#             materia__ciclo_id=ciclo_id,
#             materia_id=materia_id,
#             periodo_academico__fecha_inicio__year__lt=anio_inicio,
#         )

#         promedios = datos_historicos.aggregate(
#             Avg("cantidad_matriculados"),
#             Avg("cantidad_aprobados"),
#             Avg("cantidad_reprobados"),
#             Avg("cantidad_desertores"),
#             Avg("promedio_modalidad"),
#             Avg("promedio_tipo_educacion"),
#             Avg("promedio_origen"),
#             Avg("promedio_trabajo"),
#             Avg("promedio_discapacidad"),
#             Avg("promedio_hijos"),
#         )

#         años = list(range(anio_inicio, anio_fin + 1))
#         predicciones = {
#             "años": años,
#             "matriculados": [
#                 promedios["cantidad_matriculados__avg"] * (1 + 0.02 * i)
#                 for i in range(len(años))
#             ],
#             "aprobados": [
#                 promedios["cantidad_aprobados__avg"] * (1 + 0.01 * i)
#                 for i in range(len(años))
#             ],
#             "reprobados": [
#                 promedios["cantidad_reprobados__avg"] * (1 - 0.01 * i)
#                 for i in range(len(años))
#             ],
#             "desertores": [
#                 promedios["cantidad_desertores__avg"] * (1 - 0.02 * i)
#                 for i in range(len(años))
#             ],
#             "modalidad": [
#                 promedios["promedio_modalidad__avg"] * (1 + 0.005 * i)
#                 for i in range(len(años))
#             ],
#             "tipo_educacion": [
#                 promedios["promedio_tipo_educacion__avg"] * (1 + 0.005 * i)
#                 for i in range(len(años))
#             ],
#             "origen": [
#                 promedios["promedio_origen__avg"] * (1 + 0.005 * i)
#                 for i in range(len(años))
#             ],
#             "trabajo": [
#                 promedios["promedio_trabajo__avg"] * (1 + 0.005 * i)
#                 for i in range(len(años))
#             ],
#             "discapacidad": [
#                 promedios["promedio_discapacidad__avg"] * (1 + 0.005 * i)
#                 for i in range(len(años))
#             ],
#             "hijos": [
#                 promedios["promedio_hijos__avg"] * (1 + 0.005 * i)
#                 for i in range(len(años))
#             ],
#         }

#         return JsonResponse(predicciones)

#     return JsonResponse({"error": "Método no permitido"}, status=405)


# def ObtenerPrediccion(request):
#     facultades = Facultad.objects.all()
#     current_year = datetime.now().year
#     years = range(current_year, current_year + 20)
#     return render(
#         request, "PrediccionMateria.html", {"facultades": facultades, "years": years}
#     )


# def ObtenerPeriodosFuturos(request):
#     if request.method == "GET":
#         materia_id = request.GET.get("materia_id")

#         if not materia_id:
#             return JsonResponse(
#                 {"error": "Se requiere el ID de la materia"}, status=400
#             )

#         try:
#             materia = Materia.objects.get(id=materia_id)
#         except Materia.DoesNotExist:
#             return JsonResponse({"error": "Materia no encontrada"}, status=404)

#         fecha_actual = datetime.now().date()
#         periodos_futuros = PeriodoAcademico.objects.filter(
#             fecha_inicio__gt=fecha_actual, estado_periodo_academico="Activo"
#         ).order_by("fecha_inicio")

#         data = [
#             {
#                 "id": periodo.id,
#                 "codigo_periodo_academico": periodo.codigo_periodo_academico,
#                 "fecha_inicio": periodo.fecha_inicio.strftime("%d/%m/%Y"),
#                 "fecha_fin": periodo.fecha_fin.strftime("%d/%m/%Y"),
#             }
#             for periodo in periodos_futuros
#         ]

#         return JsonResponse(data, safe=False)

#     return JsonResponse({"error": "Método no permitido"}, status=405)

# def RungeKutta(
#     matriculados,
#     tasa_desercion,
#     tasa_aprobacion,
#     tasa_reprobacion,
#     tiempo_total,
#     num_pasos,
# ):
#     h = tiempo_total / (num_pasos - 1)
#     tiempo = np.linspace(0, tiempo_total, num_pasos)
#     resultados = np.zeros((4, num_pasos))
#     resultados[0, 0] = matriculados

#     for i in range(1, num_pasos):
#         k1 = h * (-tasa_desercion * resultados[0, i - 1])
#         k2 = h * (-tasa_desercion * (resultados[0, i - 1] + 0.5 * k1))
#         k3 = h * (-tasa_desercion * (resultados[0, i - 1] + 0.5 * k2))
#         k4 = h * (-tasa_desercion * (resultados[0, i - 1] + k3))

#         delta_matriculados = (k1 + 2 * k2 + 2 * k3 + k4) / 6
#         delta_desertores = -delta_matriculados
#         delta_aprobados = tasa_aprobacion * resultados[0, i - 1] * h
#         delta_reprobados = tasa_reprobacion * resultados[0, i - 1] * h

#         resultados[0, i] = (
#             resultados[0, i - 1]
#             + delta_matriculados
#             - delta_aprobados
#             - delta_reprobados
#         )
#         resultados[1, i] = resultados[1, i - 1] + delta_aprobados
#         resultados[2, i] = resultados[2, i - 1] + delta_reprobados
#         resultados[3, i] = resultados[3, i - 1] + delta_desertores

#     return resultados, tiempo


# def ObtenerPeriodosFuturos(request):
#     if request.method == "GET":
#         materia_id = request.GET.get("materia_id")

#         if not materia_id:
#             return JsonResponse(
#                 {"error": "Se requiere el ID de la materia"}, status=400
#             )

#         try:
#             materia = Materia.objects.get(id=materia_id)
#         except Materia.DoesNotExist:
#             return JsonResponse({"error": "Materia no encontrada"}, status=404)

#         fecha_actual = datetime.now().date()
#         periodos_futuros = PeriodoAcademico.objects.filter(
#             fecha_inicio__gt=fecha_actual, estado_periodo_academico="Activo"
#         ).order_by("fecha_inicio")

#         data = [
#             {
#                 "id": periodo.id,
#                 "codigo_periodo_academico": periodo.codigo_periodo_academico,
#                 "fecha_inicio": periodo.fecha_inicio.strftime("%d/%m/%Y"),
#                 "fecha_fin": periodo.fecha_fin.strftime("%d/%m/%Y"),
#             }
#             for periodo in periodos_futuros
#         ]

#         return JsonResponse(data, safe=False)

#     return JsonResponse({"error": "Método no permitido"}, status=405)


# def PredecirDesercion(request):
#     if request.method == "POST":
#         materia_id = request.POST.get("materia_id")
#         periodo_futuro_id = request.POST.get("periodo_futuro_id")
#         filtros = json.loads(request.POST.get("filtros"))

#         materia = Materia.objects.get(id=materia_id)
#         periodo_futuro = PeriodoAcademico.objects.get(id=periodo_futuro_id)

#         datos_historicos = DatosHistorico.objects.filter(materia=materia)

#         if not datos_historicos.exists():
#             return JsonResponse(
#                 {"error": "No hay datos históricos disponibles."}, status=400
#             )

#         promedios = datos_historicos.aggregate(
#             avg_matriculados=Avg("cantidad_matriculados"),
#             avg_aprobados=Avg("cantidad_aprobados"),
#             avg_reprobados=Avg("cantidad_reprobados"),
#             avg_desertores=Avg("cantidad_desertores"),
#             avg_modalidad=Avg("promedio_modalidad"),
#             avg_tipo_educacion=Avg("promedio_tipo_educacion"),
#             avg_origen=Avg("promedio_origen"),
#             avg_trabajo=Avg("promedio_trabajo"),
#             avg_discapacidad=Avg("promedio_discapacidad"),
#             avg_hijos=Avg("promedio_hijos"),
#         )

#         desviaciones = datos_historicos.aggregate(
#             std_matriculados=StdDev("cantidad_matriculados"),
#             std_aprobados=StdDev("cantidad_aprobados"),
#             std_reprobados=StdDev("cantidad_reprobados"),
#             std_desertores=StdDev("cantidad_desertores"),
#             std_modalidad=StdDev("promedio_modalidad"),
#             std_tipo_educacion=StdDev("promedio_tipo_educacion"),
#             std_origen=StdDev("promedio_origen"),
#             std_trabajo=StdDev("promedio_trabajo"),
#             std_discapacidad=StdDev("promedio_discapacidad"),
#             std_hijos=StdDev("promedio_hijos"),
#         )

#         num_simulaciones = 1000
#         resultados_simulacion = []

#         for _ in range(num_simulaciones):
#             matriculados = np.random.normal(
#                 promedios["avg_matriculados"], desviaciones["std_matriculados"]
#             )
#             tasa_aprobacion = np.random.normal(
#                 promedios["avg_aprobados"] / promedios["avg_matriculados"], 0.1
#             )
#             tasa_reprobacion = np.random.normal(
#                 promedios["avg_reprobados"] / promedios["avg_matriculados"], 0.1
#             )
#             tasa_desercion = np.random.normal(
#                 promedios["avg_desertores"] / promedios["avg_matriculados"], 0.1
#             )

#             factores = {
#                 "modalidad": norm.rvs(
#                     promedios["avg_modalidad"], desviaciones["std_modalidad"]
#                 ),
#                 "tipo_educacion": norm.rvs(
#                     promedios["avg_tipo_educacion"], desviaciones["std_tipo_educacion"]
#                 ),
#                 "origen": norm.rvs(promedios["avg_origen"], desviaciones["std_origen"]),
#                 "trabajo": norm.rvs(
#                     promedios["avg_trabajo"], desviaciones["std_trabajo"]
#                 ),
#                 "discapacidad": norm.rvs(
#                     promedios["avg_discapacidad"], desviaciones["std_discapacidad"]
#                 ),
#                 "hijos": norm.rvs(promedios["avg_hijos"], desviaciones["std_hijos"]),
#             }

#             if (
#                 (
#                     not filtros["modalidad"]
#                     or factores["modalidad"] > promedios["avg_modalidad"]
#                 )
#                 and (
#                     not filtros["tipo_educacion"]
#                     or factores["tipo_educacion"] > promedios["avg_tipo_educacion"]
#                 )
#                 and (
#                     not filtros["origen"]
#                     or factores["origen"] > promedios["avg_origen"]
#                 )
#                 and (
#                     not filtros["trabajo"]
#                     or factores["trabajo"] > promedios["avg_trabajo"]
#                 )
#                 and (
#                     not filtros["discapacidad"]
#                     or factores["discapacidad"] > promedios["avg_discapacidad"]
#                 )
#                 and (not filtros["hijos"] or factores["hijos"] > promedios["avg_hijos"])
#             ):

#                 # if (
#                 #     not filtros["modalidad"]
#                 #     or factores["modalidad"] > promedios["avg_modalidad"]
#                 # ) and (
#                 #     not filtros["tipo_educacion"]
#                 #     or factores["tipo_educacion"] > promedios["avg_tipo_educacion"]
#                 # ):

#                 resultados, tiempo = RungeKutta(
#                     matriculados,
#                     tasa_desercion,
#                     tasa_aprobacion,
#                     tasa_reprobacion,
#                     (periodo_futuro.fecha_fin - periodo_futuro.fecha_inicio).days,
#                     materia.unidades + 2,
#                 )

#                 resultados_simulacion.append(
#                     {"resultados": resultados, "factores": factores}
#                 )

#         resultados_promedio = np.mean(
#             [r["resultados"] for r in resultados_simulacion], axis=0
#         )
#         factores_promedio = {
#             k: np.mean([r["factores"][k] for r in resultados_simulacion])
#             for k in resultados_simulacion[0]["factores"]
#         }

#         labels = [
#             (
#                 f"Unidad {i}"
#                 if i > 0 and i <= materia.unidades
#                 else fecha.strftime("%d/%m/%Y")
#             )
#             for i, fecha in enumerate(
#                 [periodo_futuro.fecha_inicio]
#                 + [
#                     periodo_futuro.fecha_inicio + timedelta(days=int(d))
#                     for d in tiempo[1:-1]
#                 ]
#                 + [periodo_futuro.fecha_fin]
#             )
#         ]

#         data = {
#             "labels": labels,
#             "matriculados": resultados_promedio[0].tolist(),
#             "aprobados": resultados_promedio[1].tolist(),
#             "reprobados": resultados_promedio[2].tolist(),
#             "desertores": resultados_promedio[3].tolist(),
#             "titulo": f"Predicción {periodo_futuro.codigo_periodo_academico} - {materia.nombre_materia} (Ciclo {materia.ciclo.nombre_ciclo})",
#             "facultad": materia.ciclo.carrera.facultad.nombre_facultad,
#             "carrera": materia.ciclo.carrera.nombre_carrera,
#             "ciclo_nombre": materia.ciclo.nombre_ciclo,
#             "materia_nombre": materia.nombre_materia,
#             "periodo_inicio": periodo_futuro.fecha_inicio.strftime("%d/%m/%Y"),
#             "periodo_fin": periodo_futuro.fecha_fin.strftime("%d/%m/%Y"),
#             "factores": factores_promedio,
#         }

#         return JsonResponse(data)

#     return JsonResponse({"error": "Método no permitido"}, status=405)


def PRI(request):
    return render(request, "ZZ.html")


# segundo intento
# def PredecirDesercion(request):
#     if request.method == "POST":
#         materia_id = request.POST.get("materia_id")
#         periodo_futuro_id = request.POST.get("periodo_futuro_id")
#         filtros = json.loads(request.POST.get("filtros"))

#         materia = Materia.objects.get(id=materia_id)
#         periodo_futuro = PeriodoAcademico.objects.get(id=periodo_futuro_id)

#         datos_historicos = DatosHistoricos.objects.filter(materia=materia)

#         if not datos_historicos.exists():
#             return JsonResponse(
#                 {"error": "No hay datos históricos disponibles."}, status=400
#             )

#         promedios = datos_historicos.aggregate(
#             avg_matriculados=Avg("cantidad_matriculados"),
#             avg_aprobados=Avg("cantidad_aprobados"),
#             avg_reprobados=Avg("cantidad_reprobados"),
#             avg_desertores=Avg("cantidad_desertores"),
#             avg_modalidad=Avg("promedio_modalidad"),
#             avg_tipo_educacion=Avg("promedio_tipo_educacion"),
#             avg_origen=Avg("promedio_origen"),
#             avg_trabajo=Avg("promedio_trabajo"),
#             avg_discapacidad=Avg("promedio_discapacidad"),
#             avg_hijos=Avg("promedio_hijos"),
#         )

#         desviaciones = datos_historicos.aggregate(
#             std_matriculados=StdDev("cantidad_matriculados"),
#             std_aprobados=StdDev("cantidad_aprobados"),
#             std_reprobados=StdDev("cantidad_reprobados"),
#             std_desertores=StdDev("cantidad_desertores"),
#             std_modalidad=StdDev("promedio_modalidad"),
#             std_tipo_educacion=StdDev("promedio_tipo_educacion"),
#             std_origen=StdDev("promedio_origen"),
#             std_trabajo=StdDev("promedio_trabajo"),
#             std_discapacidad=StdDev("promedio_discapacidad"),
#             std_hijos=StdDev("promedio_hijos"),
#         )

#         num_simulaciones = 1000
#         resultados_simulacion = []

#         for _ in range(num_simulaciones):
#             matriculados = np.random.normal(
#                 promedios["avg_matriculados"], desviaciones["std_matriculados"]
#             )
#             tasa_aprobacion = np.random.normal(
#                 promedios["avg_aprobados"] / promedios["avg_matriculados"], 0.1
#             )
#             tasa_reprobacion = np.random.normal(
#                 promedios["avg_reprobados"] / promedios["avg_matriculados"], 0.1
#             )
#             tasa_desercion = np.random.normal(
#                 promedios["avg_desertores"] / promedios["avg_matriculados"], 0.1
#             )

#             factores = {
#                 "modalidad": norm.rvs(
#                     promedios["avg_modalidad"], desviaciones["std_modalidad"]
#                 ),
#                 "tipo_educacion": norm.rvs(
#                     promedios["avg_tipo_educacion"], desviaciones["std_tipo_educacion"]
#                 ),
#                 "origen": norm.rvs(promedios["avg_origen"], desviaciones["std_origen"]),
#                 "trabajo": norm.rvs(
#                     promedios["avg_trabajo"], desviaciones["std_trabajo"]
#                 ),
#                 "discapacidad": norm.rvs(
#                     promedios["avg_discapacidad"], desviaciones["std_discapacidad"]
#                 ),
#                 "hijos": norm.rvs(promedios["avg_hijos"], desviaciones["std_hijos"]),
#             }

#             if (
#                 (
#                     not filtros["modalidad"]
#                     or factores["modalidad"] > promedios["avg_modalidad"]
#                 )
#                 and (
#                     not filtros["tipo_educacion"]
#                     or factores["tipo_educacion"] > promedios["avg_tipo_educacion"]
#                 )
#                 and (
#                     not filtros["origen"]
#                     or factores["origen"] > promedios["avg_origen"]
#                 )
#                 and (
#                     not filtros["trabajo"]
#                     or factores["trabajo"] > promedios["avg_trabajo"]
#                 )
#                 and (
#                     not filtros["discapacidad"]
#                     or factores["discapacidad"] > promedios["avg_discapacidad"]
#                 )
#                 and (not filtros["hijos"] or factores["hijos"] > promedios["avg_hijos"])
#             ):

#                 # if (
#                 #     not filtros["modalidad"]
#                 #     or factores["modalidad"] > promedios["avg_modalidad"]
#                 # ) and (
#                 #     not filtros["tipo_educacion"]
#                 #     or factores["tipo_educacion"] > promedios["avg_tipo_educacion"]
#                 # ):

#                 resultados, tiempo = RungeKutta(
#                     matriculados,
#                     tasa_desercion,
#                     tasa_aprobacion,
#                     tasa_reprobacion,
#                     (periodo_futuro.fecha_fin - periodo_futuro.fecha_inicio).days,
#                     materia.unidades + 2,
#                 )

#                 resultados_simulacion.append(
#                     {"resultados": resultados, "factores": factores}
#                 )

#         resultados_promedio = np.mean(
#             [r["resultados"] for r in resultados_simulacion], axis=0
#         )
#         factores_promedio = {
#             k: np.mean([r["factores"][k] for r in resultados_simulacion])
#             for k in resultados_simulacion[0]["factores"]
#         }

#         labels = [
#             (
#                 f"Unidad {i}"
#                 if i > 0 and i <= materia.unidades
#                 else fecha.strftime("%d/%m/%Y")
#             )
#             for i, fecha in enumerate(
#                 [periodo_futuro.fecha_inicio]
#                 + [
#                     periodo_futuro.fecha_inicio + timedelta(days=int(d))
#                     for d in tiempo[1:-1]
#                 ]
#                 + [periodo_futuro.fecha_fin]
#             )
#         ]

#         data = {
#             "labels": labels,
#             "matriculados": resultados_promedio[0].tolist(),
#             "aprobados": resultados_promedio[1].tolist(),
#             "reprobados": resultados_promedio[2].tolist(),
#             "desertores": resultados_promedio[3].tolist(),
#             "titulo": f"Predicción {periodo_futuro.codigo_periodo_academico} - {materia.nombre_materia} (Ciclo {materia.ciclo.nombre_ciclo})",
#             "facultad": materia.ciclo.carrera.facultad.nombre_facultad,
#             "carrera": materia.ciclo.carrera.nombre_carrera,
#             "ciclo_nombre": materia.ciclo.nombre_ciclo,
#             "materia_nombre": materia.nombre_materia,
#             "periodo_inicio": periodo_futuro.fecha_inicio.strftime("%d/%m/%Y"),
#             "periodo_fin": periodo_futuro.fecha_fin.strftime("%d/%m/%Y"),
#             "factores": factores_promedio,
#         }

#         return JsonResponse(data)

#     return JsonResponse({"error": "Método no permitido"}, status=405)


# def PredecirDesercion(request):
#     if request.method == "POST":
#         materia_id = request.POST.get("materia_id")
#         materia = Materia.objects.get(id=materia_id)
#         periodo_academico = materia.ciclo.periodo_academico
#         datos_historicos = DatosHistoricos.objects.filter(materia=materia)

#         if not datos_historicos.exists():
#             return JsonResponse(
#                 {"error": "No hay datos históricos disponibles para esta materia."},
#                 status=400,
#             )

#         promedio_matriculados = datos_historicos.aggregate(
#             Avg("cantidad_matriculados")
#         )["cantidad_matriculados__avg"]
#         promedio_aprobados = datos_historicos.aggregate(Avg("cantidad_aprobados"))[
#             "cantidad_aprobados__avg"
#         ]
#         promedio_reprobados = datos_historicos.aggregate(Avg("cantidad_reprobados"))[
#             "cantidad_reprobados__avg"
#         ]
#         promedio_desertores = datos_historicos.aggregate(Avg("cantidad_desertores"))[
#             "cantidad_desertores__avg"
#         ]

#         tasa_aprobacion = promedio_aprobados / promedio_matriculados
#         tasa_reprobacion = promedio_reprobados / promedio_matriculados
#         tasa_desercion = promedio_desertores / promedio_matriculados

#         matriculados_iniciales = int(promedio_matriculados)
#         unidades = materia.unidades
#         dias_periodo = (
#             periodo_academico.fecha_fin - periodo_academico.fecha_inicio
#         ).days

#         tiempo = np.linspace(0, dias_periodo, unidades + 2)
#         matriculados = np.zeros(len(tiempo))
#         aprobados = np.zeros(len(tiempo))
#         reprobados = np.zeros(len(tiempo))
#         desertores = np.zeros(len(tiempo))

#         matriculados[0] = matriculados_iniciales

#         for i in range(1, len(tiempo)):
#             delta_tiempo = tiempo[i] - tiempo[i - 1]
#             delta_desertores = (
#                 tasa_desercion * matriculados[i - 1] * delta_tiempo / dias_periodo
#             )
#             delta_aprobados = (
#                 tasa_aprobacion * matriculados[i - 1] * delta_tiempo / dias_periodo
#             )
#             delta_reprobados = (
#                 tasa_reprobacion * matriculados[i - 1] * delta_tiempo / dias_periodo
#             )

#             desertores[i] = desertores[i - 1] + delta_desertores
#             aprobados[i] = aprobados[i - 1] + delta_aprobados
#             reprobados[i] = reprobados[i - 1] + delta_reprobados
#             matriculados[i] = matriculados[i - 1] - delta_desertores

#         total_final = aprobados[-1] + reprobados[-1] + desertores[-1]
#         factor_ajuste = matriculados_iniciales / total_final

#         aprobados *= factor_ajuste
#         reprobados *= factor_ajuste
#         desertores *= factor_ajuste

#         matriculados_finales = int(matriculados[-1])
#         aprobados_finales = int(aprobados[-1])
#         reprobados_finales = int(reprobados[-1])
#         desertores_finales = int(desertores[-1])

#         diferencia = matriculados_iniciales - (
#             aprobados_finales + reprobados_finales + desertores_finales
#         )
#         aprobados_finales += diferencia

#         labels = [
#             f"Unidad {i}" if i > 0 and i <= unidades else fecha.strftime("%d/%m/%Y")
#             for i, fecha in enumerate(
#                 [periodo_academico.fecha_inicio]
#                 + [
#                     periodo_academico.fecha_inicio + timedelta(days=int(d))
#                     for d in tiempo[1:-1]
#                 ]
#                 + [periodo_academico.fecha_fin]
#             )
#         ]

#         data = {
#             "labels": labels,
#             "matriculados": matriculados.tolist(),
#             "aprobados": aprobados.tolist(),
#             "reprobados": reprobados.tolist(),
#             "desertores": desertores.tolist(),
#             "titulo": f"Predicción {periodo_academico.codigo_periodo_academico} - {materia.nombre_materia} (Ciclo {materia.ciclo.nombre_ciclo})",
#             "facultad": materia.ciclo.carrera.facultad.nombre_facultad,
#             "carrera": materia.ciclo.carrera.nombre_carrera,
#             "ciclo_nombre": materia.ciclo.nombre_ciclo,
#             "materia_nombre": materia.nombre_materia,
#             "periodo_inicio": periodo_academico.fecha_inicio.strftime("%d/%m/%Y"),
#             "periodo_fin": periodo_academico.fecha_fin.strftime("%d/%m/%Y"),
#             "promedio_modalidad": datos_historicos.aggregate(Avg("promedio_modalidad"))[
#                 "promedio_modalidad__avg"
#             ]
#             or 0,
#             "promedio_tipo_educacion": datos_historicos.aggregate(
#                 Avg("promedio_tipo_educacion")
#             )["promedio_tipo_educacion__avg"]
#             or 0,
#             "promedio_origen": datos_historicos.aggregate(Avg("promedio_origen"))[
#                 "promedio_origen__avg"
#             ]
#             or 0,
#             "promedio_trabajo": datos_historicos.aggregate(Avg("promedio_trabajo"))[
#                 "promedio_trabajo__avg"
#             ]
#             or 0,
#             "promedio_discapacidad": datos_historicos.aggregate(
#                 Avg("promedio_discapacidad")
#             )["promedio_discapacidad__avg"]
#             or 0,
#             "promedio_hijos": datos_historicos.aggregate(Avg("promedio_hijos"))[
#                 "promedio_hijos__avg"
#             ]
#             or 0,
#             "matriculados_iniciales": matriculados_iniciales,
#             "matriculados_finales": matriculados_finales,
#             "aprobados_finales": aprobados_finales,
#             "reprobados_finales": reprobados_finales,
#             "desertores_finales": desertores_finales,
#         }

#         return JsonResponse(data)

#     return JsonResponse({"error": "Método no permitido"}, status=405)
