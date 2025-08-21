from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/auth_register.html"
    success_url = reverse_lazy("home")  # ajusta si tu home se llama distinto

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')   # cambialo si tu inicio tiene otro name

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)        # inicia sesión automáticamente
        return redirect(self.get_success_url())

