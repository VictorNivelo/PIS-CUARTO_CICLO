from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password1', 'password2']