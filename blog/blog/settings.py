import os
from dotenv import load_dotenv

load_dotenv()

DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .configurations.production import *
else:
    from .configurations.local import *


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.post.apps.PostConfig",
    "apps.user.apps.UserConfig",
    "apps.accounts",
]


LOGIN_REDIRECT_URL = "post:post_list"
LOGOUT_REDIRECT_URL = "post:post_list"
LOGIN_URL = "post:login"