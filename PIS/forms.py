from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    DatosHistoricos,
    Genero,
    InformeCarrera,
    InformeMateria,
    TipoDNI,
    UsuarioPersonalizado,
    Universidad,
    Facultad,
    Carrera,
    Materia,
    Ciclo,
    PeriodoAcademico,
    Estudiante,
)


class TelefonoInput(forms.TextInput):
    input_type = "tel"

    def __init__(self, attrs=None):
        default_attrs = {"pattern": "[0-9]{1,10}", "maxlength": "13"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class RegistrarUsuarioForm(UserCreationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        max_length=100,
        required=True,
        label="Correo Electrónico",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su nombre"}),
        max_length=100,
        required=True,
        label="Nombre",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su apellido"}),
        max_length=100,
        required=True,
        label="Apellido",
    )

    genero = forms.ModelChoiceField(
        queryset=Genero.objects.all(),
        to_field_name="nombre_genero",
        empty_label="Seleccione un genero",
        required=True,
        label="Genero",
    )

    telefono = forms.CharField(
        widget=TelefonoInput(attrs={"placeholder": "Ingrese su número de teléfono"}),
        max_length=10,
        required=True,
        label="Numero de teléfono",
    )

    tipo_dni = forms.ModelChoiceField(
        queryset=TipoDNI.objects.all(),
        to_field_name="nombre_tipo_dni",
        empty_label="Seleccione un Tipo de DNI",
        required=True,
        label="Tipo de DNI",
    )

    dni = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su DNI"}),
        max_length=10,
        required=True,
        label="DNI",
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "Placeholder": "Ingrese su fecha de nacimiento",
            }
        ),
        required=True,
        label="Fecha de Nacimiento",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
        required=True,
        label="Contraseña",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme su contraseña"}),
        required=True,
        label="Confirmar Contraseña",
    )

    rol = forms.ChoiceField(
        choices=UsuarioPersonalizado.ROLES,
        initial="Docente",
        required=False,
        label="Rol",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = [
            "username",
            "first_name",
            "last_name",
            "genero",
            "telefono",
            "tipo_dni",
            "dni",
            "fecha_nacimiento",
            "password1",
            "password2",
        ]
        widgets = {
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }


class RegistrarEstudianteForm(forms.ModelForm):
    tipo_dni = forms.ModelChoiceField(
        queryset=TipoDNI.objects.all(),
        to_field_name="nombre_tipo_dni",
        empty_label="Seleccione un Tipo de DNI",
        required=True,
        label="Tipo de DNI",
    )

    dni_estudiante = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su DNI"}),
        max_length=10,
        required=True,
        label="DNI",
    )

    nombre_estudiante = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su nombre"}),
        max_length=100,
        required=True,
        label="Nombre",
    )

    apellido_estudiante = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su apellido"}),
        max_length=100,
        required=True,
        label="Apellido",
    )

    genero = forms.ModelChoiceField(
        queryset=Genero.objects.all(),
        to_field_name="nombre_genero",
        empty_label="Seleccione un genero",
        required=True,
        label="Genero",
    )

    modalidad_estudio = forms.ChoiceField(
        choices=Estudiante.MODALIDAD_ESTUDIO_CHOICES,
        required=True,
        label="Modalidad de Estudio",
    )

    tipo_educacion = forms.ChoiceField(
        choices=Estudiante.TIPO_EDUCACION_CHOICES,
        required=True,
        label="Tipo de Educación",
    )

    origen = forms.ChoiceField(
        choices=Estudiante.ORIGEN_CHOICES,
        required=True,
        label="Origen",
    )

    trabajo = forms.ChoiceField(
        choices=Estudiante.TRABAJA_CHOICES,
        required=True,
        label="Trabajo",
    )

    discapacidad = forms.ChoiceField(
        choices=Estudiante.DISCAPACIDAD_CHOICES,
        required=True,
        label="Discapacidad",
    )

    hijos = forms.ChoiceField(
        choices=Estudiante.HIJOS_CHOICES,
        required=True,
        label="Hijos",
    )

    estado = forms.ChoiceField(
        choices=Estudiante.ESTADO_CHOICES,
        required=True,
        label="Estado",
    )

    class Meta:
        model = Estudiante
        fields = [
            "tipo_dni",
            "estado",
            "dni_estudiante",
            "nombre_estudiante",
            "apellido_estudiante",
            "genero",
            "modalidad_estudio",
            "tipo_educacion",
            "origen",
            "trabajo",
            "discapacidad",
            "hijos",
            "materia",
        ]


class TipoDNIForm(forms.ModelForm):
    nombre_tipo_dni = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el nombre del tipo de DNI"}
        ),
        max_length=100,
        required=True,
        label="Nombre del Tipo de DNI",
    )

    descripcion_tipo_dni = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese la descripción del tipo de DNI"}
        ),
        max_length=100,
        required=True,
        label="Descripción",
    )

    class Meta:
        model = TipoDNI
        fields = ["nombre_tipo_dni", "descripcion_tipo_dni"]


class GeneroForm(forms.ModelForm):
    nombre_genero = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese el nombre del genero"}),
        max_length=100,
        required=True,
        label="Nombre del Genero",
    )

    descripcion_genero = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese la descripción del genero"}
        ),
        max_length=100,
        required=True,
        label="Descripción",
    )

    class Meta:
        model = Genero
        fields = ["nombre_genero", "descripcion_genero"]


class InicioSesionForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        required=True,
        label="Correo Electrónico",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
        required=True,
        label="Contraseña",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["username", "password"]


class RecuperarContraseniaForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        required=True,
        label="Correo Electrónico",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["username"]


class CambiarContraseniaForm(forms.ModelForm):
    Contrasenia = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Ingrese la nueva contraseña"}
        ),
        required=True,
        label="Contraseña",
    )

    Confirmar_contrasenia = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirme la nueva contraseña"}
        ),
        required=True,
        label="Confirmar Contraseña",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Contrasenia", "Confirmar_contrasenia"]

    def clean(self):
        cleaned_data = super().clean()
        Contrasenia = cleaned_data.get("Contrasenia")
        Confirmar_contrasenia = cleaned_data.get("Confirmar_contrasenia")

        if (
            Contrasenia
            and Confirmar_contrasenia
            and Contrasenia != Confirmar_contrasenia
        ):
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class ModificarCorreoForm(forms.ModelForm):
    Correo = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        required=True,
        label="Correo Electrónico",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Correo"]


class ModificarRolUsuarioForm(forms.ModelForm):
    rol = forms.ChoiceField(
        choices=[
            ("Personal Administrativo", "Personal Administrativo"),
            ("Secretaria", "Secretaria"),
            ("Docente", "Docente"),
        ],
        required=True,
        label="Rol",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["rol"]
        widgets = {"rol": forms.Select(choices=UsuarioPersonalizado.ROLES)}


class UniversidadForm(forms.ModelForm):
    nombre_universidad = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el nombre de la universidad"}
        ),
        max_length=100,
        required=True,
        label="Nombre de la Universidad",
    )

    direccion_universidad = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese la dirección de la universidad"}
        ),
        max_length=100,
        required=True,
        label="Dirección",
    )

    telefono_universidad = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el teléfono de la universidad"}
        ),
        max_length=13,
        required=True,
        label="Teléfono",
    )

    correo_universidad = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Ingrese el correo de la universidad"}
        ),
        required=True,
        label="Correo",
    )

    fecha_fundacion = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fundacion"}
        ),
        required=True,
        label="Fecha de Creación",
    )

    class Meta:
        model = Universidad
        fields = [
            "nombre_universidad",
            "direccion_universidad",
            "telefono_universidad",
            "correo_universidad",
            "fecha_fundacion",
        ]


class FacultadForm(forms.ModelForm):
    nombre_facultad = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el nombre de la facultad"}
        ),
        max_length=100,
        required=True,
        label="Nombre de la Facultad",
    )

    fecha_fundacion = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fundacion"}
        ),
        required=True,
        label="Fecha de Creación",
    )

    universidad = forms.ModelChoiceField(
        queryset=Universidad.objects.all(),
        to_field_name="nombre_universidad",
        empty_label="Seleccione una universidad",
        label="Universidad",
    )

    class Meta:
        model = Facultad
        fields = [
            "nombre_facultad",
            "fecha_fundacion",
            "universidad",
        ]


class CarreraForm(forms.ModelForm):
    nombre_carrera = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el nombre de la carrera"}
        ),
        max_length=100,
        required=True,
        label="Nombre de la Carrera",
    )

    duracion = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese la duración de la carrera en ciclos"}
        ),
        min_value=1,
        required=True,
        label="Duración",
    )

    facultad = forms.ModelChoiceField(
        queryset=Facultad.objects.all(),
        to_field_name="nombre_facultad",
        empty_label="Seleccione una facultad",
        required=True,
        label="Facultad",
    )

    class Meta:
        model = Carrera
        fields = [
            "nombre_carrera",
            "duracion",
            "facultad",
        ]


class CicloForm(forms.ModelForm):
    nombre_ciclo = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese el nombre del ciclo"}),
        max_length=100,
        required=True,
        label="Nombre del Ciclo",
    )

    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de inicio"}
        ),
        required=True,
        label="Fecha de Inicio",
    )

    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fin"}
        ),
        required=True,
        label="Fecha de Fin",
    )

    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        to_field_name="nombre_carrera",
        empty_label="Seleccione una carrera",
        required=True,
        label="Carrera",
    )

    class Meta:
        model = Ciclo
        fields = [
            "nombre_ciclo",
            "fecha_inicio",
            "fecha_fin",
            "carrera",
        ]


class MateriaForm(forms.ModelForm):
    nombre_materia = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el nombre de la materia"}
        ),
        required=True,
        label="Nombre de la Materia",
    )

    numero_horas = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Ingrese el número de horas"}),
        min_value=1,
        required=True,
        label="Número de Horas",
    )

    unidades = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese el número de unidades"}
        ),
        required=True,
        min_value=1,
        label="Unidades",
    )

    docente_encargado = forms.ModelChoiceField(
        queryset=UsuarioPersonalizado.objects.filter(rol="Docente"),
        to_field_name="username",
        empty_label="Seleccione un docente",
        required=True,
        label="Docente Encargado",
    )

    ciclo = forms.ModelChoiceField(
        queryset=Ciclo.objects.all(),
        to_field_name="nombre_ciclo",
        empty_label="Seleccione un ciclo",
        required=True,
        label="Ciclo",
    )

    periodo_academico = forms.ModelChoiceField(
        queryset=PeriodoAcademico.objects.all(),
        to_field_name="codigo_periodo_academico",
        empty_label="Seleccione un periodo académico",
        required=True,
        label="Periodo Académico",
    )

    # datos_historicos = forms.ModelChoiceField(
    #     queryset=Datos_Historicos.objects.all(),
    #     to_field_name="codigo_datos_historicos",
    #     empty_label="Seleccione datos historicos",
    #     label="Datos Historicos",
    # )

    class Meta:
        model = Materia
        fields = [
            "nombre_materia",
            "numero_horas",
            "unidades",
            "docente_encargado",
            "ciclo",
            "periodo_academico",
        ]


class PeriodoAcademicoForm(forms.ModelForm):
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de inicio"}
        ),
        required=True,
        label="Fecha de Inicio",
    )

    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fin"}
        ),
        required=True,
        label="Fecha de Fin",
    )

    ESTADO_CHOICES = [
        ("Activo", "Activo"),
        ("Inactivo", "Inactivo"),
    ]

    estado_periodo_academico = forms.ChoiceField(choices=ESTADO_CHOICES, required=True, label="Estado")

    class Meta:
        model = PeriodoAcademico
        fields = [
            "fecha_inicio",
            "fecha_fin",
            "estado_periodo_academico",
        ]

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError(
                "La fecha de inicio no puede ser después de la fecha de fin."
            )

        return cleaned_data


class DatosHistoricosForm(forms.ModelForm):

    # materia = forms.ModelChoiceField(
    #     queryset=Materia.objects.all(),
    #     to_field_name="nombre_materia",
    #     empty_label="Seleccione una materia",
    #     required=True,
    #     label="Materia",
    # )

    cantidad_matriculados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese la cantidad de matriculados"}
        ),
        min_value=0,
        required=True,
        label="Cantidad de Matriculados",
    )

    cantidad_aprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese la cantidad de aprovados"}
        ),
        min_value=0,
        required=True,
        label="Cantidad de Aprobados",
    )

    cantidad_reprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese la cantidad de reprovados"}
        ),
        min_value=0,
        required=True,
        label="Cantidad de Reprobados",
    )

    cantidad_desertores = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese la cantidad de desertores"}
        ),
        min_value=0,
        required=True,
        label="Cantidad de Desertores",
    )

    class Meta:
        model = DatosHistoricos
        fields = [
            "cantidad_matriculados",
            "cantidad_aprobados",
            "cantidad_reprobados",
            "cantidad_desertores",
        ]


# Formularios de informes


class InformeCarreraForm(forms.ModelForm):
    Carrera = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el nombre de la carrera",
            }
        ),
        required=True,
        label="Carrera",
    )

    Numero_estudiantes = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de estudiantes",
            }
        ),
        required=True,
        label="Número de Estudiantes",
    )

    Aprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la cantidad de aprobados",
            }
        ),
        required=True,
        label="Aprobados",
    )

    Reprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la cantidad de reprobados",
            }
        ),
        required=True,
        label="Reprobados",
    )

    Desertores = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la cantidad de desertores",
            }
        ),
        required=True,
        label="Desertores",
    )

    Retirados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese la cantidad de retirados",
            }
        ),
        required=True,
        label="Retirados",
    )

    class Meta:
        model = InformeCarrera
        fields = [
            "Carrera",
            "Numero_estudiantes",
            "Aprobados",
            "Reprobados",
            "Desertores",
            "Retirados",
        ]


class InformeCicloForm(forms.Form):
    ciclo = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el ciclo",
            }
        ),
        required=True,
        label="Ciclo",
    )

    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Seleccione la fecha de inicio",
            }
        ),
        required=True,
        label="Fecha de Inicio",
    )

    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Seleccione la fecha de fin",
            }
        ),
        required=True,
        label="Fecha de Fin",
    )

    numero_estudiantes = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de estudiantes",
            }
        ),
        required=True,
        label="Número de Estudiantes",
    )

    aprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de aprobados",
            }
        ),
        required=True,
        label="Aprobados",
    )

    reprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de reprobados",
            }
        ),
        required=True,
        label="Reprobados",
    )

    desertores = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de desertores",
            }
        ),
        required=True,
        label="Desertores",
    )

    retirados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de retirados",
            }
        ),
        required=True,
        label="Retirados",
    )


class InformeMateriaForm(forms.ModelForm):
    materia = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre de la materia",
            }
        ),
        required=True,
        label="Materia",
    )

    docente_encargado = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre del docente encargado",
            }
        ),
        required=True,
        label="Docente Encargado",
    )

    numero_estudiantes = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes",
            }
        ),
        required=True,
        label="Número de Estudiantes",
    )

    aprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes aprobados",
            }
        ),
        required=True,
        label="Aprobados",
    )

    reprobados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes reprobados",
            }
        ),
        required=True,
        label="Reprobados",
    )

    desertores = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes desertores",
            }
        ),
        required=True,
        label="Desertores",
    )

    retirados = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes retirados",
            }
        ),
        required=True,
        label="Retirados",
    )

    class Meta:
        model = InformeMateria
        fields = [
            "materia",
            "docente_encargado",
            "numero_estudiantes",
            "aprobados",
            "reprobados",
            "desertores",
            "retirados",
        ]
