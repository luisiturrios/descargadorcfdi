"""
Django settings for descargador project.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# APP CONFIG
DEBUG = True

SECRET_KEY = 'vac64ha47f__kfepydv(m18q1%!#5zfw7*(=ss4*r6$ty)6_x5'

ALLOWED_HOSTS = [
    'descargador.k8shub.tk'
]

ROOT_URLCONF = 'descargador.urls'

WSGI_APPLICATION = 'descargador.wsgi.application'

DEFAULT_CHARSET = 'utf-8'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_celery_results',
    'django_celery_beat',
    'crispy_forms',
    'auth2',
    'descargadorweb',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'descargador',
        'USER': 'user001',
        'PASSWORD': 'j2FvHyzkZ3FJwHJU',
        'HOST': 'db',
        'PORT': '3306',
        'CHARSET': 'utf8mb4',
        'COLLATION': 'utf8mb4_unicode_ci',
    }
}

# LOCALIZATION
LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_INPUT_FORMATS = ['%d/%m/%Y', ]

# FILES
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# AUTHENTICATION
LOGIN_URL = 'auth2:login'

LOGIN_REDIRECT_URL = 'descargadorweb:empresas'

LOGOUT_REDIRECT_URL = 'descargadorweb:index'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CRISPY
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# CELERY
CELERY_BROKER_URL = 'redis://broker:6379/0'
CELERY_RESULT_BACKEND = 'django-db'

try:
    from local_settings import *
except ImportError:
    pass
