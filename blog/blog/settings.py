# blog/settings.py
from pathlib import Path
import os

# --- Opcional: dotenv (no rompe si no existe) ---
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- Rutas base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Básicos ---
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")  # cambia en prod
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = ['https://nexusgaming.pythonanywhere.com','NexusGaming.pythonanywhere.com', 'nexusgaming.pythonanywhere.com']

# --- Apps ---
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Tus apps
    "apps.user.apps.UserConfig",  # usuario custom
    "apps.accounts",              # cuentas/roles/señales
    "apps.post",                  # blog

    # Dev tools (opcional: instalar 'django-browser-reload')
    "django_browser_reload",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django_browser_reload.middleware.BrowserReloadMiddleware",  # si lo usás
]

# --- URLs/WGI ---
ROOT_URLCONF = "blog.urls"
WSGI_APPLICATION = "blog.wsgi.application"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # carpeta /templates a nivel proyecto
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- Base de datos (dev) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv('DB_NAME'),

        'USER': os.getenv('DB_USER'),

        'PASSWORD': os.getenv('DB_PASSWORD'),

        'HOST': os.getenv('DB_HOST'),

        'PORT': os.getenv('DB_PORT'),


    }
}

# --- Password validators (dev simplificado) ---
AUTH_PASSWORD_VALIDATORS = []  # agrega validadores en prod si querés

# --- Localización ---
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Cordoba"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos y media ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # comentá si no tenés carpeta
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Usuario custom ---
AUTH_USER_MODEL = "user.User"

# --- Login / Logout ---
LOGIN_URL = "login"              # o "user:login" si usás namespace
LOGIN_REDIRECT_URL = "home"      # dejalo a tu vista inicial
LOGOUT_REDIRECT_URL = "home"

# --- Email (dev) ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@nexus.local"
