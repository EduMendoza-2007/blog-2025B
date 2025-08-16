from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/auth_register.html"
    success_url = reverse_lazy("home")  # ajusta si tu home se llama distinto
