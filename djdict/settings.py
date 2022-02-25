"""
Django settings for djdict project.

Generated by 'django-admin startproject' usign Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Set your secret key in environment variables, in development you can use a string right away for convenience
SECRET_KEY = os.environ.get("SECRET_KEY", "Not a secret! Delete this arg in production!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: don't allow any other hosts except your real host in production!
ALLOWED_HOSTS = ["134.209.81.163","mobilasyon.com","www.mobilasyon.com","localhost","127.0.0.1"]

GRAPHENE = {"SCHEMA": "dictionary_graph.schema.schema"}

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "djdict",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django built-in
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.sitemaps",
    # Main apps
    "dictionary",
    "django.contrib.admin",
    "dictionary_graph",
    # Third Party
    "graphene_django",
    "widget_tweaks",
    "djcelery_email",
    "djcelery",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Using custom csrf middleware here. Check the module to see the rationale.
    "dictionary.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",

    "dictionary.middleware.users.NoviceActivityMiddleware",
    "dictionary.middleware.frontend.MobileDetectionMiddleware",  # 1
    "dictionary.middleware.frontend.LeftFrameMiddleware",  # 2
]

ROOT_URLCONF = "djdict.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dictionary.utils.context_processors.header_categories",
                "dictionary.utils.context_processors.left_frame_fallback",
            ],
        },
    },
]

WSGI_APPLICATION = "djdict.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": "mobilasyondb"
#         }
#     }
# else:
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mobilasyondb',
            'USER': 'mobilasyon_admin',
            'PASSWORD': '159357741369asd',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


AUTH_USER_MODEL = "dictionary.Author"
LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"

SESSION_COOKIE_AGE = 1209600

# WARNING: Use "dictionary.backends.sessions.cached_db" engine for improved
# performance if you have the cache server (memcached etc.) set up and running.
SESSION_ENGINE = "dictionary.backends.sessions.db"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "mobilasyonsozluk@gmail.com"
EMAIL_HOST_PASSWORD = "cbdligwxtzqiojyl"
EMAIL_USE_TLS = True

REDIS_URL = "redis://127.0.0.1:6379"
CELERY_BROKER_URL = REDIS_URL
# CELERY_EMAIL_TASK_CONFIG = {"default_retry_delay": 40}
CELERY_EMAIL_TASK_CONFIG = {
    'name': 'djcelery_email_send',
    'ignore_result': False,
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

LANGUAGE_COOKIE_NAME = "langcode"
LANGUAGE_COOKIE_AGE = 180 * 86400
LANGUAGE_COOKIE_SAMESITE = "Lax"

USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ("tr", _("Turkish")),
    ("en", _("English")),
)


PASSWORD_RESET_TIMEOUT = 86400
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
