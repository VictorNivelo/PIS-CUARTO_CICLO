from django import forms
from .models import UsuarioPersonalizado


class RegistrarUsuarioForm(forms.ModelForm):
    Contrasenia = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    Confirmar_Contrasenia = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar Contraseña"
    )

    class Meta:
        model = UsuarioPersonalizado
        fields = ["username", "email", "Contrasenia"]

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


class UsuarioInicioSesionForm(forms.ModelForm):
    Correo = forms.EmailField()
    Contrasenia = forms.CharField(widget=forms.PasswordInput)


class RecuperarContraseniaForm(forms.ModelForm):
    Correo = forms.EmailField()


class CambiarContraseniaForm(forms.ModelForm):
    Contrasenia = forms.CharField(widget=forms.PasswordInput)
    Confirmar_contrasenia = forms.CharField(widget=forms.PasswordInput)


class ModificarCorreoForm(forms.ModelForm):
    Correo = forms.EmailField()


class ModificarRolUsuarioForm(forms.ModelForm):
    Rol = forms.ChoiceField(
        choices=[
            ("personal_Administrativo", "Personal Administrativo"),
            ("secretaria", "Secretaria"),
            ("docente", "Docente"),
        ]
    )


# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = CustomUser
#         fields = ["username", "email", "password", "confirm_password"]

# class RegistrarUsuarioForm(forms.ModelForm):
#     Usuario = forms.CharField()
#     Correo = forms.EmailField()
#     Contrasenia = forms.CharField(widget=forms.PasswordInput)
#     Confirmar_contrasenia = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = UsuarioPersonalizado
#         fields = ["Usuario", "Correo", "Contrasenia", "Confirmar_Contrasenia"]
