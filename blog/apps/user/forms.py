from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from apps.user.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'alias', 'avatar')

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(
            attrs={'class': 'form-control', 
                   'placeholder': 'Username'
                   }
                )
            )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )