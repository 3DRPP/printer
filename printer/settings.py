"""
Django settings for printer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _
DEFAULT_CHARTSET = 'utf-8'

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'assets')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Site
SITE_NAME = "3DRPP"
DOMAIN = 'http://localhost/' # Must end with a slash! /!\
SITE_URL_PREFIX = '' # Empty or your-prefix/ <- Must end with a slash /!\
SITE_URL = DOMAIN + SITE_URL_PREFIX
STATIC_URL = '/' + SITE_URL_PREFIX + 'assets/'
MEDIA_URL = '/' + SITE_URL_PREFIX + 'media/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5dxu%_2qv*nvhal*oa!b=qr-x94^26ax2y@t$aukemdkve^)4r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

AUTH_USER_MODEL = 'printer.User'
PASSWORD_HASHERS = ('django.contrib.auth.hashers.PBKDF2PasswordHasher',)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'printer'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'printer.urls'

WSGI_APPLICATION = 'printer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# I18N
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
LANGUAGES = (
    ('fr', _('French')),
)

USE_I18N = False
USE_L10N = True
USE_TZ = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'printer.context_processors.site_infos'
            ],
        },
    },
]

GPIO_pins = {
    7: None,
    8: None,
    10: None,
    11: None,
    12: None,
    13: None,
    15: None,
    16: None,
    18: None,
    19: None,
    21: None,
    22: None,
    23: None,
    24: None,
    26: None,
    29: None,
    31: {
        'target': 'X-axis-sensor',
        'mode': 'in',
        'default': False,
        'events': None
    },
    32: {
        'target': 'Y-axis-sensor',
        'mode': 'in',
        'default': False,
        'events': None
    },
    33: {
        'target': 'Z-axis-sensor',
        'mode': 'in',
        'default': False,
        'events': None
    },
    35: {
        'target': 'ventilation',
        'mode': 'out',
        'default': False
    },
    36: {
        'target': 'beeper',
        'mode': 'out',
        'default': False
    },
    37: {
        'target': 'nozzle-heating',
        'mode': 'out',
        'default': False
    },
    38: {
        'target': 'heating-bed',
        'mode': 'out',
        'default': False
    },
    40: {
        'target': 'alimentation',
        'mode': 'out',
        'default': False
    }
}

live_stream = {
    'activated': True,
    'url': 'http://192.168.1.22:8080/stream/video.mjpeg'
}

printer = {
    'dimensions': {
        'X-axis': 300.00, #mm
        'Y-axis': 300.00, #mm
        'Z-axis': 300.00  #mm
    },
    'nozzle': {
        'temperature-sensor': {
            '/dev': 'TODO'
        }
    },
    'heating-bed': {
        'temperature-sensor': {
            '/dev': 'TODO'
        }
    },
    'motor-hats': {
        'below': {
            'addr': 0x60,
            'freq': 1600,
            'm1-m2': {
                'name': 'X-axis',
                'step': 1.80, #degrees
                'speed': 30 #rpm
            },
            'm3-m4': {
                'name': 'Y-axis',
                'step': 1.80, #degrees
                'speed': 30 #rpm
            }
        },
        'above': {
            'addr': 0x61,
            'freq': 1600,
            'm1-m2': {
                'name': 'Z-axis',
                'step': 1.80, #degrees
                'speed': 30 #rpm
            },
            'm3-m4': {
                'name': 'nozzle',
                'step': 1.80, #degrees
                'speed': 30 #rpm
            }
        }
    }
}