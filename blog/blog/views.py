from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from apps.post.models import Post

class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'
    
    def get_queryset(self):
        #obtener los ultimos tres recientes
        return Post.objects.order_by('-created_at')[:3]

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/auth_register.html"
    success_url = reverse_lazy("home")  # ajusta si tu home se llama distinto

class AboutView(TemplateView):
    template_name = 'about_us.html'

from django.shortcuts import render

def contact_view(request):
    return render(request, 'contact.html')

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings

from .forms import ContactForm


class ContactView(FormView):
    template_name = "contact.html"   
    form_class = ContactForm
    success_url = reverse_lazy("contact_ok")

    def form_valid(self, form):
        data = form.cleaned_data
        subject = data.get("subject") or "[Contacto del blog]"
        body = (
            f"Nombre: {data['name']}\n"
            f"Email: {data['email']}\n"
            f"Consentimiento: {'sí' if data.get('consent') else 'no'}\n\n"
            f"Mensaje:\n{data['message']}"
        )
        send_mail(
            subject=subject,
            message=body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[getattr(settings, "CONTACT_EMAIL_TO", "admin@example.com")],
            fail_silently=True,  
        )
        return super().form_valid(form)


class ContactOKView(TemplateView):
    template_name = "contact_ok.html"
