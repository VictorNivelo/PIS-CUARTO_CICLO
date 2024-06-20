from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    InformeCarrera,
    InformeMateria,
    UsuarioPersonalizado,
    Universidad,
    Facultad,
    Carrera,
    Materia,
    Ciclo,
)


class RegistrarUsuarioForm(UserCreationForm):

    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        label="Correo Electrónico",
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su nombre"}),
        label="Nombre",
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su apellido"}),
        label="Apellido",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
        label="Contraseña",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirme su contraseña"}),
        label="Confirmar Contraseña",
    )

    genero = forms.ChoiceField(
        choices=UsuarioPersonalizado.GENERO_OPCIONES, required=False, label="Género"
    )

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "Placeholder": "Ingrese su fecha de nacimiento",
            }
        ),
        required=False,
        label="Fecha de Nacimiento",
    )

    tipo_dni = forms.ChoiceField(
        choices=UsuarioPersonalizado.TIPO_DNI_OPCIONES,
        required=False,
        label="Tipo de identificacion",
    )

    dni = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su DNI"}),
        max_length=10,
        required=False,
        label="DNI",
    )

    telefono = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su número de teléfono"}),
        max_length=10,
        required=False,
        label="Numero de teléfono",
    )

    rol = forms.ChoiceField(
        choices=UsuarioPersonalizado.ROLES,
        required=False,
        initial="Docente",
        label="Rol",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "genero",
            "fecha_nacimiento",
            "tipo_dni",
            "dni",
            "telefono",
        ]
        widgets = {
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }


class InicioSesionForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        label="Correo Electrónico",
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su contraseña"}),
        label="Contraseña",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["username", "password"]


class RecuperarContraseniaForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        label="Correo Electrónico",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["username"]


class CambiarContraseniaForm(forms.ModelForm):
    Contrasenia = forms.CharField(widget=forms.PasswordInput)
    Confirmar_contrasenia = forms.CharField(widget=forms.PasswordInput)

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
    Correo = forms.EmailField()

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
        label="Nombre de la Universidad",
    )
    direccion_universidad = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese la dirección de la universidad"}
        ),
        label="Dirección",
    )
    telefono_universidad = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el teléfono de la universidad"}
        ),
        label="Teléfono",
    )
    correo_universidad = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Ingrese el correo de la universidad"}
        ),
        label="Correo",
    )
    fecha_fundacion = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fundacion"}
        ),
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
        label="Nombre de la Facultad",
    )
    fecha_fundacion = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fundacion"}
        ),
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
        label="Nombre de la Carrera",
    )
    duracion = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "Ingrese la duración de la carrera en horas"}
        ),
        label="Duración",
        min_value=1,
    )
    facultad = forms.ModelChoiceField(
        queryset=Facultad.objects.all(),
        to_field_name="nombre_facultad",
        empty_label="Seleccione una facultad",
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
        label="Nombre del Ciclo",
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de inicio"}
        ),
        label="Fecha de Inicio",
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "placeholder": "Ingrese la fecha de fin"}
        ),
        label="Fecha de Fin",
    )
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        to_field_name="nombre_carrera",
        empty_label="Seleccione una carrera",
        label="Carrera",
    )

    class Meta:
        model = Carrera
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
        label="Nombre de la Materia",
    )
    numero_horas = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Ingrese el número de horas"}),
        label="Número de Horas",
    )
    docente_encargado = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Ingrese el nombre del docente encargado"}
        ),
        label="Docente Encargado",
    )
    ciclo = forms.ModelChoiceField(
        queryset=Ciclo.objects.all(),
        to_field_name="nombre_ciclo",
        empty_label="Seleccione un ciclo",
        label="Ciclo",
    )

    class Meta:
        model = Materia
        fields = [
            "nombre_materia",
            "numero_horas",
            "docente_encargado",
            "ciclo",
        ]


# Formularios de informes


class InformeCarreraForm(forms.ModelForm):
    Carrera = forms.CharField(
        label="Carrera",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el nombre de la carrera",
            }
        ),
    )
    Numero_estudiantes = forms.IntegerField(
        label="Número de Estudiantes",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el número de estudiantes",
            }
        ),
    )
    Aprobados = forms.IntegerField(
        label="Aprobados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese la cantidad de aprobados",
            }
        ),
    )
    Reprobados = forms.IntegerField(
        label="Reprobados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese la cantidad de reprobados",
            }
        ),
    )
    Desertores = forms.IntegerField(
        label="Desertores",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese la cantidad de desertores",
            }
        ),
    )
    Retirados = forms.IntegerField(
        label="Retirados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese la cantidad de retirados",
            }
        ),
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
        label="Ciclo",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el ciclo",
            }
        ),
    )
    fecha_inicio = forms.DateField(
        label="Fecha de Inicio",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Seleccione la fecha de inicio",
            }
        ),
    )
    fecha_fin = forms.DateField(
        label="Fecha de Fin",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Seleccione la fecha de fin",
            }
        ),
    )
    numero_estudiantes = forms.IntegerField(
        label="Número de Estudiantes",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el número de estudiantes",
            }
        ),
    )
    aprobados = forms.IntegerField(
        label="Aprobados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el número de aprobados",
            }
        ),
    )
    reprobados = forms.IntegerField(
        label="Reprobados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el número de reprobados",
            }
        ),
    )
    desertores = forms.IntegerField(
        label="Desertores",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el número de desertores",
            }
        ),
    )
    retirados = forms.IntegerField(
        label="Retirados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "required": True,
                "placeholder": "Ingrese el número de retirados",
            }
        ),
    )


class InformeMateriaForm(forms.ModelForm):
    Materia = forms.CharField(
        label="Materia",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre de la materia",
                "required": True,
            }
        ),
    )
    Docente_encargado = forms.CharField(
        label="Docente Encargado",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre del docente encargado",
                "required": True,
            }
        ),
    )
    Num_estudiantes = forms.IntegerField(
        label="Número de Estudiantes",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes",
                "required": True,
            }
        ),
    )
    Aprobados = forms.IntegerField(
        label="Aprobados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes aprobados",
                "required": True,
            }
        ),
    )
    Reprobados = forms.IntegerField(
        label="Reprobados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes reprobados",
                "required": True,
            }
        ),
    )
    Desertores = forms.IntegerField(
        label="Desertores",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes desertores",
                "required": True,
            }
        ),
    )
    Retirados = forms.IntegerField(
        label="Retirados",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad de estudiantes retirados",
                "required": True,
            }
        ),
    )

    class Meta:
        model = InformeMateria
        fields = [
            "Materia",
            "Docente_encargado",
            "Num_estudiantes",
            "Aprobados",
            "Reprobados",
            "Desertores",
            "Retirados",
        ]
