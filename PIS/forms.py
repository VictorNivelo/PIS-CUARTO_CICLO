from django import forms
from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "confirm_password"]


# Nuevos valores


class RegistrarUsuarioForm(forms.ModelForm):
    Correo = forms.EmailField()
    Contrasenia = forms.charField(widget=forms.PasswordInput)
    Confirmar_contrasenia = forms.charField(widget=forms.PasswordInput)


class UsuarioInicioSesionForm(forms.ModelForm):
    Correo = forms.EmailField()
    Contrasenia = forms.charField(widget=forms.PasswordInput)


class RecuperarContraseniaForm(forms.ModelForm):
    Correo = forms.EmailField()


class CambiarContraseniaForm(forms.ModelForm):
    Contrasenia = forms.charField(widget=forms.PasswordInput)
    Confirmar_contrasenia = forms.charField(widget=forms.PasswordInput)


class ModificarCorreoForm(forms.ModelForm):
    Correo = forms.EmailField()


class ModidicarRolUsuarioForm(forms.ModelForm):
    Rol = forms.ChoiceField(
        choices=[
            ("personal_Administrativo", "PersonalAdministrativo"),
            ("secretaria", "Secretaria"),
            ("docente", "Docente"),
        ]
    )
