from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

class IndexView(TemplateView):
    template_name = 'index.html'

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/auth_register.html"
    success_url = reverse_lazy("home")  # ajusta si tu home se llama distinto

class AboutView(TemplateView):
    template_name = 'about_us.html'
