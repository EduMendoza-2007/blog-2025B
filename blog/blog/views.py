from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'post/post_list.html'

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.urls import path

class IndexView(TemplateView):
    template_name = "post/post_list.html"

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/auth_register.html"
    success_url = reverse_lazy("home")  # ajusta si tu home se llama distinto


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]
