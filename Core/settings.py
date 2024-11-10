
from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = Path.joinpath(BASE_DIR, 'templates')
STATIC_DIR = Path.joinpath(BASE_DIR, 'static')
MEDIA_DIR = Path.joinpath(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gz#7qi643+%c8=v+id*t$2$_ou&*aakos+gmyc%laxn(93-9$('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# SECRET_KEY = config('THE_SECRET_KEY')
# DEBUG = config('WEB_DEBUG', cast = bool)

ALLOWED_HOSTS = ['*']
# CSRF_TRUSTED_ORIGINS = ['']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App_Auth',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': 
    [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
        'DEFAULT_PERMISSION_CLASSES':
    [
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend']
}

ROOT_URLCONF = 'Core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'Core.wsgi.application'

AUTH_USER_MODEL = 'App_Auth.User'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DATABASE_NAME'),
#         'HOST': config("DATABASE_HOST"),
#         'PORT': config("DATABASE_PORT"),
#         'USER': config("DATABASE_USER"),
#         'PASSWORD': config("DATABASE_PASSWORD"),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_ROOT = ''

# STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = 'media/'
MEDIA_ROOT = MEDIA_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# from datetime import timedelta
# AUTO_LOGOUT = {
#     'IDLE_TIME': timedelta(minutes=30),
#     #  'SESSION_TIME': timedelta(minutes=30),
#     'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
#      'MESSAGE': 'The session has expired. Please login again to continue.',
# }


# ### Send Mail 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'exploreuniversemystery@gmail.com'
EMAIL_HOST_PASSWORD = 'ygfwaiubmlbkbffm'

# ### Lockdown Password
# LOCKDOWN_PASSWORDS = ('letmein', 'beta')

### Cross Site Scripting 
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

### Redirects all non-HTTPS requests to HTTP
# SECURE_SSL_REDIRECT = True

### HTTP Strict Transport Security
# SECURE_HSTS_SECONDS = 86400
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

### Cross-site request forgery(CSRF) protection
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

