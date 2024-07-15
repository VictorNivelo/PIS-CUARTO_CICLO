import csv
import json
import token
from django.views import View
from django.views.decorators.http import require_http_methods
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
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from docx import Document
from django.db import transaction
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
from .Modelo.ModeloMatematico import model, params_list
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
    DatosHistoricos,
)
from .forms import (
    DatosHistoricosForm,
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


@csrf_exempt
@require_http_methods(["GET", "POST"])
def RegistrarUsuario(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = RegistrarUsuarioForm(data)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                if UsuarioPersonalizado.objects.filter(username=user.username).exists():
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "El correo electrónico ya está registrado.",
                        }
                    )

                if UsuarioPersonalizado.objects.filter(dni=user.dni).exists():
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "El número de DNI ya está registrado.",
                        }
                    )

                num_usuarios = UsuarioPersonalizado.objects.count()
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
            error_message = "Por favor, corrija los siguientes errores:"
            if "username" in form.errors:
                error_message = "El correo electrónico ya está registrado."
            elif "dni" in form.errors:
                error_message = "El número de DNI ya está registrado."
            else:
                error_message = "Por favor, verifique los datos ingresados."

            return JsonResponse({"status": "error", "message": error_message})
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


def ImportarEstudiante(request):
    if request.method == "POST":
        csv_file = request.FILES.get("archivo_csv")
        if not csv_file.name.endswith(".csv"):
            messages.error(request, "El archivo debe ser formato CSV.")
            return redirect("Gestion_Estudiante")

        csv_data = csv.reader(csv_file.read().decode("utf-8").splitlines())

        next(csv_data, None)

        for row in csv_data:
            tipo_dni_nombre = [0].strip()
            dni_estudiante = row[1].strip()
            nombre_estudiante = row[2].strip()
            apellido_estudiante = row[3].strip()
            genero_nombre = row[4].strip()
            modalidad_estudio = int(row[5].strip())
            tipo_educacion = int(row[6].strip())
            origen = int(row[7].strip())
            trabajo = int(row[8].strip())
            discapacidad = int(row[9].strip())
            hijos = int(row[10].strip())
            materias_nombres = [m.strip() for m in row[11].split(",")]

            try:
                tipo_dni = TipoDNI.objects.get(nombre_tipo_dni=tipo_dni_nombre)
            except TipoDNI.DoesNotExist:
                messages.error(
                    request, f'El tipo de DNI "{tipo_dni_nombre}" no existe.'
                )
                return redirect("Gestion_Estudiante")

            try:
                genero = Genero.objects.get(nombre_genero=genero_nombre)
            except Genero.DoesNotExist:
                messages.error(request, f'El género "{genero_nombre}" no existe.')
                return redirect("Gestion_Estudiante")

            estudiante = Estudiante(
                tipo_dni=tipo_dni,
                dni_estudiante=dni_estudiante,
                nombre_estudiante=nombre_estudiante,
                apellido_estudiante=apellido_estudiante,
                genero=genero,
                modalidad_estudio=modalidad_estudio,
                tipo_educacion=tipo_educacion,
                origen=origen,
                trabajo=trabajo,
                discapacidad=discapacidad,
                hijos=hijos,
            )
            estudiante.save()

            for materia_nombre in materias_nombres:
                try:
                    materia = Materia.objects.get(nombre_materia=materia_nombre)
                    estudiante.materia.add(materia)
                except Materia.DoesNotExist:
                    messages.warning(
                        request,
                        f'La materia "{materia_nombre}" no existe. No se agregó.',
                    )

        messages.success(
            request, "Estudiantes importados exitosamente desde el archivo CSV."
        )
        return redirect("Gestion_Estudiante")

    return render(request, "SubirEstudiante.html")


def CorreoEnviado(request, uidb64, token):
    return render(request, "CorreoRecuperacionEnviado.html")


User = get_user_model()


def RecuperarContrasenia(request):
    if request.method == "POST":
        form = RecuperarContraseniaForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data["username"]
            try:
                user = UsuarioPersonalizado.objects.get(username=username_or_email)
            except User.DoesNotExist:
                try:
                    user = UsuarioPersonalizado.objects.get(email=username_or_email)
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
    periodosAcademicos = PeriodoAcademico.objects.all()
    docentes = UsuarioPersonalizado.objects.filter(rol="Docente")

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
                docente = UsuarioPersonalizado.objects.get(id=docente_encargado_id)
                ciclo = Ciclo.objects.get(id=ciclo_id)

                materia.periodo_academico = periodo
                materia.docente_encargado = docente
                materia.ciclo = ciclo

                materia.save()
                messages.success(request, "Materia actualizada exitosamente.")

            except (
                PeriodoAcademico.DoesNotExist,
                UsuarioPersonalizado.DoesNotExist,
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
            datos_historicos = form.save(commit=False)
            datos_historicos.save()
            messages.success(request, "Datos históricos registrados exitosamente.")
            return redirect("Gestion_DatosHistorico")
        else:
            messages.error(request, "Por favor, corrija los errores del formulario.")
    else:
        form = DatosHistoricosForm()

    return render(request, "RDH-CrearDatosHistoricos.html", {"form": form})


def GestionDatosHistoricos(request):
    query = request.GET.get("search_query", "")
    datos_Historicos = DatosHistoricos.objects.all()

    if query:
        datos_Historicos = datos_Historicos.filter(
            Q(cantidad_matriculados__icontains=query)
        )

    if request.method == "POST":
        if "modify" in request.POST:
            datos_historicos_id = request.POST.get("datos_historicos_id")
            datos_historicos = DatosHistoricos.objects.get(id=datos_historicos_id)
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

            datos_historicos.save()
            messages.success(request, "Dato histórico actualizado exitosamente.")

        elif "delete" in request.POST:
            datos_historicos_id = request.POST.get("datos_historicos_id")
            datos_historicos = DatosHistoricos.objects.get(id=datos_historicos_id)
            datos_historicos.delete()
            messages.success(request, "Dato histórico eliminado exitosamente.")

        return redirect("Gestion_DatosHistorico")

    return render(
        request,
        "GestionDatosHistoricos.html",
        {
            "datos_Historicos": datos_Historicos,
            "query": query,
        },
    )


# Funcionalidad de subir archivo para su procesamiento


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


def predecir_desercion(request):
    facultades = Facultad.objects.all()
    return render(request, "predecir.html", {"facultades": facultades})


def obtener_carreras(request):
    facultad_id = request.GET.get("facultad_id")
    carreras = Carrera.objects.filter(facultad_id=facultad_id).values(
        "id", "nombre_carrera"
    )
    return JsonResponse({"carreras": list(carreras)})


def obtener_ciclos(request):
    carrera_id = request.GET.get("carrera_id")
    ciclos = Ciclo.objects.filter(carrera_id=carrera_id).values("id", "nombre_ciclo")
    return JsonResponse({"ciclos": list(ciclos)})


def obtener_materias(request):
    ciclo_id = request.GET.get("ciclo_id")
    materias = Materia.objects.filter(ciclo_id=ciclo_id).values("id", "nombre_materia")
    return JsonResponse({"materias": list(materias)})


def realizar_prediccion(request):
    materia_id = request.GET.get("materia_id")

    materia = Materia.objects.get(id=materia_id)
    estudiantes = Estudiante.objects.filter(materia=materia)
    total_estudiantes = estudiantes.count()
    desertores = estudiantes.filter(estado="Desertor").count()
    cursando = estudiantes.filter(estado="Cursando").count()
    aprobado = estudiantes.filter(estado="Aprobado").count()
    reprobado = estudiantes.filter(estado="Reprobado").count()

    data = {
        "nombre_materia": materia.nombre_materia,
        "total_estudiantes": total_estudiantes,
        "desertores": desertores,
        "cursando": cursando,
        "aprobado": aprobado,
        "reprobado": reprobado,
    }

    return JsonResponse({"prediccion": data})


# class PrediccionDesercionView(View):

#     def runge_kutta_4(self, f, t0, y0, t_final, h, params):
#         t = np.arange(t0, t_final + h, h)
#         n = len(t)
#         y = np.zeros((n, len(y0)))
#         y[0] = y0

#         for i in range(1, n):
#             k1 = h * f(t[i - 1], y[i - 1], params)
#             k2 = h * f(t[i - 1] + 0.5 * h, y[i - 1] + 0.5 * k1, params)
#             k3 = h * f(t[i - 1] + 0.5 * h, y[i - 1] + 0.5 * k2, params)
#             k4 = h * f(t[i - 1] + h, y[i - 1] + k3, params)

#             y[i] = y[i - 1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6

#         return t, y

#     def sistema_ecuaciones(self, t, y, params):
#         S, R, D, A = y
#         dSdt = -0.1 * S
#         dRdt = 0.1 * S - 0.05 * R
#         dDdt = 0.05 * R
#         dAdt = 0.1 * R
#         return [dSdt, dRdt, dDdt, dAdt]

#     def get(self, request):
#         universidades = Universidad.objects.all()

#         universidad_id = request.GET.get("universidad")
#         facultad_id = request.GET.get("facultad")
#         carrera_id = request.GET.get("carrera")
#         ciclo_id = request.GET.get("ciclo")
#         materia_id = request.GET.get("materia")

#         universidad = (
#             get_object_or_404(Universidad, id=universidad_id)
#             if universidad_id
#             else None
#         )
#         facultad = get_object_or_404(Facultad, id=facultad_id) if facultad_id else None
#         carrera = get_object_or_404(Carrera, id=carrera_id) if carrera_id else None
#         ciclo = get_object_or_404(Ciclo, id=ciclo_id) if ciclo_id else None
#         materia = get_object_or_404(Materia, id=materia_id) if materia_id else None

#         periodo_academico = PeriodoAcademico.objects.filter(
#             estado_periodo_academico="activo"
#         ).first()

#         if (
#             universidad
#             and facultad
#             and carrera
#             and ciclo
#             and materia
#             and periodo_academico
#         ):
#             datos_historicos = Datos_Historicos.objects.filter(
#                 estudiante__materia=materia,
#                 estudiante__ciclo=ciclo,
#                 estudiante__tipo_educacion=carrera.tipo_educacion,
#                 estudiante__trabajo=carrera.trabajo,
#                 estudiante__discapacidad=carrera.discapacidad,
#                 estudiante__hijos=carrera.hijos,
#                 estudiante__genero=carrera.genero,
#                 periodo_academico=periodo_academico,
#             ).first()

#             if datos_historicos:
#                 t0 = 0
#                 y0 = [1000, 0, 0, 0]
#                 t_final = 50
#                 h = 0.1

#                 params = {}

#                 t, y = self.runge_kutta_4(
#                     self.sistema_ecuaciones, t0, y0, t_final, h, params
#                 )

#                 data = {
#                     "universidades": universidades,
#                     "universidad_seleccionada": universidad,
#                     "facultad_seleccionada": facultad,
#                     "carrera_seleccionada": carrera,
#                     "ciclo_seleccionado": ciclo,
#                     "materia_seleccionada": materia,
#                     "periodo_academico": periodo_academico,
#                     "t": t.tolist(),
#                     "S": y[:, 0].tolist(),
#                     "R": y[:, 1].tolist(),
#                     "D": y[:, 2].tolist(),
#                     "A": y[:, 3].tolist(),
#                 }

#                 return render(request, "prediccion_desercion.html", data)

#         return render(
#             request,
#             "error.html",
#             {
#                 "mensaje": "No se encontraron datos históricos válidos para la predicción"
#             },
#         )


def prediccion_desercion(request):
    universidades = Universidad.objects.all()
    facultades = Facultad.objects.all()
    carreras = Carrera.objects.all()
    ciclos = Ciclo.objects.all()
    materias = Materia.objects.all()

    universidad_seleccionada = None
    facultad_seleccionada = None
    carrera_seleccionada = None
    ciclo_seleccionado = None
    materia_seleccionada = None

    if request.method == "GET":
        universidad_id = request.GET.get("universidad")
        facultad_id = request.GET.get("facultad")
        carrera_id = request.GET.get("carrera")
        ciclo_id = request.GET.get("ciclo")
        materia_id = request.GET.get("materia")

        if universidad_id:
            universidad_seleccionada = Universidad.objects.get(pk=universidad_id)
            facultades = Facultad.objects.filter(universidad=universidad_seleccionada)

        if facultad_id:
            facultad_seleccionada = Facultad.objects.get(pk=facultad_id)
            carreras = Carrera.objects.filter(facultad=facultad_seleccionada)

        if carrera_id:
            carrera_seleccionada = Carrera.objects.get(pk=carrera_id)
            ciclos = Ciclo.objects.filter(carrera=carrera_seleccionada)

        if ciclo_id:
            ciclo_seleccionado = Ciclo.objects.get(pk=ciclo_id)
            materias = Materia.objects.filter(ciclo=ciclo_seleccionado)

        if materia_id:
            materia_seleccionada = Materia.objects.get(pk=materia_id)

    context = {
        "universidades": universidades,
        "facultades": facultades,
        "carreras": carreras,
        "ciclos": ciclos,
        "materias": materias,
        "universidad_seleccionada": universidad_seleccionada,
        "facultad_seleccionada": facultad_seleccionada,
        "carrera_seleccionada": carrera_seleccionada,
        "ciclo_seleccionado": ciclo_seleccionado,
        "materia_seleccionada": materia_seleccionada,
    }

    if materia_seleccionada and ciclo_seleccionado:
        datos_historicos = DatosHistoricos.objects.filter(materia=materia_seleccionada)
        t = [
            datetime.date.today() + datetime.timedelta(days=i)
            for i in range(len(datos_historicos))
        ]
        S = [dh.cantidad_estudiantes for dh in datos_historicos]
        R = [dh.cantidad_aprobados for dh in datos_historicos]
        D = [dh.cantidad_desertores for dh in datos_historicos]
        A = [dh.cantidad_retirados for dh in datos_historicos]

        def model(t, y):
            S, R, D, A = y
            dSdt = -0.1 * S
            dRdt = 0.1 * S
            dDdt = 0.05 * S
            dAdt = 0.05 * S
            return [dSdt, dRdt, dDdt, dAdt]

        y0 = [S[0], R[0], D[0], A[0]]
        sol = solve_ivp(model, [0, len(t)], y0, t_eval=t)

        context.update(
            {
                "t": sol.t.tolist(),
                "S": sol.y[0].tolist(),
                "R": sol.y[1].tolist(),
                "D": sol.y[2].tolist(),
                "A": sol.y[3].tolist(),
            }
        )

    return render(request, "prediccion_desercion.html", context)


class SeleccionarDatosView(View):
    def get(self, request):
        universidades = Universidad.objects.all()
        return render(
            request, "seleccionar_datos.html", {"universidades": universidades}
        )


class PrediccionView(View):
    def post(self, request):
        universidad_id = request.POST.get("universidad")
        facultades = Facultad.objects.filter(universidad_id=universidad_id)
        return render(request, "seleccionar_datos.html", {"facultades": facultades})


class CarreraView(View):
    def post(self, request):
        facultad_id = request.POST.get("facultad")
        carreras = Carrera.objects.filter(facultad_id=facultad_id)
        return render(request, "seleccionar_datos.html", {"carreras": carreras})


class CicloView(View):
    def post(self, request):
        carrera_id = request.POST.get("carrera")
        ciclos = Ciclo.objects.filter(carrera_id=carrera_id)
        return render(request, "seleccionar_datos.html", {"ciclos": ciclos})


class MateriaView(View):
    def post(self, request):
        ciclo_id = request.POST.get("ciclo")
        materias = Materia.objects.filter(ciclo_id=ciclo_id)
        return render(request, "seleccionar_datos.html", {"materias": materias})


class PeriodoAcademicoView(View):
    def post(self, request):
        materia_id = request.POST.get("materia")
        periodos = (
            PeriodoAcademico.objects.all()
        )  # Aquí puedes filtrar los periodos según tus criterios
        return render(request, "seleccionar_datos.html", {"periodos": periodos})


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
                if model == UsuarioPersonalizado:
                    genero = get_or_create_related(Genero, nombre_genero=row["genero"])
                    tipo_dni = get_or_create_related(
                        TipoDNI, nombre_tipo_dni=row["tipo_dni"]
                    )
                    instance = UsuarioPersonalizado(
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
                        UsuarioPersonalizado, username=row["docente_encargado"]
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

                elif model == DatosHistoricos:
                    materia = get_or_create_related(
                        Materia, nombre_materia=row["materia"]
                    )
                    instance = DatosHistoricos(
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


def import_data(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        model_name = request.POST.get("model_name")

        if not csv_file:
            messages.error(request, "Por favor, seleccione un archivo CSV.")
            return redirect("import_data")

        if not model_name:
            messages.error(request, "Por favor, seleccione un modelo.")
            return redirect("import_data")

        model_map = {
            "usuario": UsuarioPersonalizado,
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
            return redirect("import_data")

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

        return redirect("import_data")

    return render(request, "import_data.html")


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
                    instance = UsuarioPersonalizado(
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
                    instance = Ciclo(
                        nombre_ciclo=row["nombre_ciclo"],
                        numero_ciclo=row["numero_ciclo"],
                        fecha_inicio=row["fecha_inicio"],
                        fecha_fin=row["fecha_fin"],
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
                    periodo_academico = get_or_create_related(
                        PeriodoAcademico,
                        codigo_periodo_academico=row["periodo_academico"],
                    )
                    docente = get_or_create_related(
                        UsuarioPersonalizado, username=row["docente_encargado"]
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
                    # materia = get_or_create_related(
                    #     Materia, nombre_materia=row["materia"]
                    # )
                    instance = DatosHistoricos(
                        # para futuro
                        # materia=materia,
                        cantidad_matriculados=int(row["cantidad_matriculados"]),
                        cantidad_aprobados=int(row["cantidad_aprobados"]),
                        cantidad_reprobados=int(row["cantidad_reprobados"]),
                        cantidad_desertores=int(row["cantidad_desertores"]),
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
                    "message": f"Se importaron {created_count} datos historicos, pero hubo algunos errores.",
                }
            )
        return JsonResponse(
            {
                "success": True,
                "message": f"Se importaron exitosamente {created_count} datos historicos.",
            }
        )
    except Exception as e:
        return JsonResponse({"success": False, "errors": [str(e)]})
