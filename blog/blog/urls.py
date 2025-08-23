from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog.views import IndexView
from .views import AboutView, contact_view
from blog.views import IndexView, AboutView, ContactView, ContactOKView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path("about_us/", AboutView.as_view(), name="about_us"),
    path("contacto/", ContactView.as_view(), name="contact"), 
    path("contacto/gracias/", ContactOKView.as_view(), name="contact_ok"),
    path('', include('apps.post.urls')),      
    path('', include('apps.user.urls')),      
    path("", include("apps.accounts.urls")),  
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
