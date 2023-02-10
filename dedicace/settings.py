"""
Django settings for dedicace project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import datetime
import os
from pathlib import Path

import dj_database_url
import whitenoise.storage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&_*hcuw7w45=i4-5=%((h2efryk8_^(eqzb*q-2x2*_5%_i*tt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://dedicace.fly.dev',
    'https://41a1-105-235-136-72.eu.ngrok.io',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "knox",
    'main',
    'chat',
    'dashboard'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

REST_KNOX = {
    'AUTO_REFRESH': True,
    'TOKEN_TTL':    datetime.timedelta(days=90)
}

AUTHENTICATION_BACKENDS = [
    'main.auth.UserAuthBackend',
    'main.auth.UserAuthUsernameIsPhone',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'dedicace.urls'

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [
            BASE_DIR / 'templates',
            BASE_DIR / 'dashboard/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING = {
    'version':                  1,
    'disable_existing_loggers': False,
    'handlers':                 {
        'stream':    {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'file':      {
            'level':    'INFO',
            'class':    'logging.FileHandler',
            'filename': 'chat.log'
        },
        'main_file': {
            'level':    'INFO',
            'class':    'logging.FileHandler',
            'filename': 'main.log'
        },
    },
    'loggers':                  {
        'chat': {
            'level':    'INFO',
            'handlers': ['stream', 'file']
        },
        'main': {
            'level':    "DEBUG",
            'handlers': ['stream', 'main_file']
        }
    }
}

WSGI_APPLICATION = 'dedicace.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse("postgres://postgres:cfPqoXAeNS8zwAa@dedicace-db.internal:5433/dedicace")
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "main.User"

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Algiers'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'dashboard/static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
FILE_UPLOAD_PERMISSIONS = 0o644
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
