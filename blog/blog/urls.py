from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog.views import IndexView
from .views import AboutView

urlpatterns = [
        path('admin/', admin.site.urls),

    # Home
    path('', IndexView.as_view(), name='home'),
    path("about_us/", AboutView.as_view(), name="about_us"),

    # Rutas de tu app de posts (si las tenés)
    path('', include('apps.post.urls')),       # SIN namespace aquí

    # Rutas de usuario en la raíz (login, logout, signup...)
    path('', include('apps.user.urls')),       # ← DEJÁ ESTA
    # path('user/', include('apps.user.urls', namespace='user')),  # ← QUITAR esta línea
    path("", include("apps.accounts.urls")),  # login/logout/signup y vistas de roles
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
