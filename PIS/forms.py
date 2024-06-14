from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import InformeCarrera, InformeMateria, UsuarioPersonalizado


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

    rol = forms.ChoiceField(
        choices=[
            ("personal_Administrativo", "Personal Administrativo"),
            ("secretaria", "Secretaria"),
            ("docente", "Docente"),
        ],
        initial="docente",
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
            "rol",
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
            ("personal_Administrativo", "Personal Administrativo"),
            ("secretaria", "Secretaria"),
            ("docente", "Docente"),
        ]
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["username", "rol"]
        widgets = {
            "username": forms.TextInput(attrs={"readonly": "readonly"}),
        }


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
