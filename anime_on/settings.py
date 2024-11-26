"""
Django settings for anime_on project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import sys
import logging
from anime_on.utils import to_bool, to_list
from datetime import timedelta
from rest_framework.settings import api_settings


logger = logging.getLogger(__name__)


PROJECT_VERSION = '##VERSION##'

ENV_NAME = os.environ.get('ENV_NAME', 'DEV').upper()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secure-test-key-1')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = to_bool(os.environ.get('DEBUG'))  # turned off by default
TESTING = "test" in sys.argv
DEBUG_TOOLBAR_ENABLED = DEBUG and not TESTING

ALLOWED_HOSTS = to_list(os.getenv('ALLOWED_HOSTS'))
if ALLOWED_HOSTS and "*" not in ALLOWED_HOSTS:
    CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS]

CORS_ALLOW_HEADERS = to_list(os.getenv('CORS_ALLOW_HEADERS'))

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    # 'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    # apps
    'apps.user',
    'apps.authentication',
    'apps.anime',
    'apps.comment',
    'apps.core',
    'apps.support',
    # libraries
    'storages',
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_admin_inline_paginator',
    'django_countries',
    'django_filters',
    'adminfilters',
    'rangefilter',
    'django_extensions',
    'admin_auto_filters',
]

MIDDLEWARE = [
    'apps.core.middleware.ping_middleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'apps.core.middleware.request_id_middleware',
    'apps.core.middleware.error_logging_middleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PARSER_CLASSES': [
        'apps.core.parsers.JSONParser',  # overridden
        'rest_framework.parsers.FormParser',  # by default
        'rest_framework.parsers.MultiPartParser'  # by default
    ],
    'EXCEPTION_HANDLER': 'apps.core.views.custom_exception_handler'
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

ROOT_URLCONF = 'anime_on.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['apps.support.templatetags.support']
        },
    },
]

WSGI_APPLICATION = 'anime_on.wsgi.application'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = os.getenv('STATIC_URL', 'static/')
STATIC_ROOT = os.getenv('STATIC_ROOT', 'static_dir/')
STATICFILES_DIRS = (BASE_DIR / 'static',)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {  # It's not used, actually. The logic is overridden in the 'finalise_deploy' command
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# AWS Configuration
AWS_LOCATION = os.getenv('AWS_LOCATION', '').lstrip("/")

if AWS_STORAGE_BUCKET_NAME:
    STORAGES['default']['BACKEND'] = 'storages.backends.s3boto3.S3Boto3Storage'
    STORAGES['staticfiles']['BACKEND'] = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_SIGNATURE_VERSION = 's3v4'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PG_DB'),
        'USER': os.environ.get('PG_USER'),
        'PASSWORD': os.environ.get('PG_PASSWORD'),
        'HOST': os.environ.get('PG_HOST'),
        'PORT': os.environ.get('PG_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

SWAGGER_ENABLED = to_bool(os.environ.get('SWAGGER_ENABLED'))  # turned off by default

SWAGGER_SETTINGS = {
    # https://drf-yasg.readthedocs.io/en/stable/settings.html#default-model-rendering
    'DEFAULT_MODEL_RENDERING': 'example',
    'DEFAULT_MODEL_DEPTH': 4,
    'DEEP_LINKING': True,
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

if DEBUG_TOOLBAR_ENABLED:
    import socket

    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG
    }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}

# INFO logs required to capture log events and metric
# can be increased to ERROR on dev environments to save us from the global warming
LOGGER_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {"()": 'anime_on.logging.FormatterJSON'},
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            # django, django.request, django.server must be redefined, otherwise they log their text by default
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
        },
        'django.request': {  # this is for access logs and unhandled exceptions
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
            'propagate': False,
        },
        'django.server': {  # this is for local use only, I expect
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {  # default handler
            'handlers': ['console'],
            'level': LOGGER_LEVEL,
            'propagate': True
        },
    },
}

# https://habr.com/ru/sandbox/128490/ іформація про те, як вимкнути захист
# використання почти з різних девайсів
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = to_bool(os.getenv("EMAIL_USE_TLS"))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

LOGIN_URL = '/api/auth/login/'

DEFAULT_EXCEPTION_REPORTER = 'apps.core.debug.JSONExceptionReporter'
DEFAULT_EXCEPTION_REPORTER_FILTER = 'apps.core.debug.JSONSafeExceptionReporterFilter'

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
SQS_QUEUE_ARN = os.getenv('SQS_QUEUE_ARN')
if not SQS_QUEUE_ARN:
    logger.error("'SQS_QUEUE_ARN' is not defined. Async tasks schedules will be ignored")
SCHEDULER_RUN_TASK_ROLE_ARN = os.getenv('SCHEDULER_RUN_TASK_ROLE_ARN')
if not SCHEDULER_RUN_TASK_ROLE_ARN:
    logger.error("'SCHEDULER_RUN_TASK_ROLE_ARN' is not defined. Async tasks schedules will be ignored")
