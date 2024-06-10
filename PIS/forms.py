from django import forms
from .models import UsuarioPersonalizado


class RegistrarUsuarioForm(forms.ModelForm):
    Nombre = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su nombre"}),
        label="Nombre de Usuario",
    )
    Apellido = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Ingrese su apellido"}),
        label="Apellido de Usuario",
    )
    Correo = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electrónico"}),
        label="Correo Electrónico",
    )
    Contrasenia = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su constraseña"}),
        label="Contraseña",
    )
    Confirmar_Contrasenia = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su constraseña"}),
        label="Confirmar Contraseña",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Nombre", "Apellido", "Correo", "Contrasenia", "Confirmar_Contrasenia"]

    def clean(self):
        cleaned_data = super().clean()
        Contrasenia = cleaned_data.get("Contrasenia")
        Confirmar_Contrasenia = cleaned_data.get("Confirmar_Contrasenia")

        if (
            Contrasenia
            and Confirmar_Contrasenia
            and Contrasenia != Confirmar_Contrasenia
        ):
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class InicioSesionForm(forms.ModelForm):
    Correo = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electronico"}),
        label="Correo Electrónico",
    )
    Contrasenia = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Ingrese su constraseña"}),
        label="Contraseña",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Correo", "Contrasenia"]


class RecuperarContraseniaForm(forms.ModelForm):
    Correo = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Ingrese su correo electronico"}),
        label="Correo Electrónico",
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Correo"]


class CambiarContraseniaForm(forms.ModelForm):
    Contrasenia = forms.CharField(widget=forms.PasswordInput)
    Confirmar_contrasenia = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Contrasenia", "Confirmar_contrasenia"]


class ModificarCorreoForm(forms.ModelForm):
    Correo = forms.EmailField()

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Correo"]


class ModificarRolUsuarioForm(forms.ModelForm):
    Rol = forms.ChoiceField(
        choices=[
            ("personal_Administrativo", "Personal Administrativo"),
            ("secretaria", "Secretaria"),
            ("docente", "Docente"),
        ]
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["Rol"]
