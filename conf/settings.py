"""
Django settings for CRMv2 project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.obspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c9*&51$bgn^+mjtak$got(o(%k!n10=&x5)n0_6fkw$tz7o#le'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','192.168.1.30']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Libs
    'widget_tweaks',
    # Aplicaciones
    'app.cobros',
    'app.homepage',
    'app.login',
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

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],   #se coloca os.path.join(BASE_DIR, 'templates') para q busq la carpeta templates
        'APP_DIRS': True, # esto si deseamos que busque en los templates de nuestras aplicaciones
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cobros',
        'USER': 'root',
        'PASSWORD': 'Art3aga_1',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-hn'

TIME_ZONE = 'America/Tegucigalpa'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# declaración de variable para usar archivos estáticos

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"), # _global
]

# para el login hay q indicarle a que URL nos dirigirá si es exitoso
LOGIN_REDIRECT_URL = '/cobros/dashboard/'

# para q direcciones en caso de darle salir sesión
LOGOUT_REDIRECT_URL = '/login/'

# en caso de querer ingresar a una URL ya existente y no está loggeado un usuario que me direccione a:
LOGIN_URL = '/login/'

# Para alojar nuestros archivos media usamos:
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
#creamos la URL absoluta para acceder
MEDIA_URL = '/media/'