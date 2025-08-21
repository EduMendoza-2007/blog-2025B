from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from apps.user.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'alias', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField (
        max_length=150, 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Usuario'
                   }
                )
            )
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'}
        )
    )