from django.views.generic import TemplateView

# Create your views here.
class UserProfileView(TemplateView):
    template_name = 'user/user_profile.html'