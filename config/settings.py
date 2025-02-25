"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-+hed&-k3i%ni(v&7wrupgx@kcvjw=#fditfl$4=*&2lblm=*ce')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'leadzz-production.up.railway.app,localhost,127.0.0.1,localhost:8000').split(',')
    


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',  # Make sure this is here
    'allauth', 'allauth.account', 'allauth.socialaccount',
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
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'app' / 'templates',  # Explicitly add your app's template dir
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            # 'debug': True,  # Add this line
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',  # Ensure this matches your actual database name
        'USER': 'postgres',  # Ensure this matches your actual database user
        'PASSWORD': 'ZOFiPzLwYQExrvZGosndbPbhovLFCFUj',  # Ensure this is set correctly
        'HOST': 'shortline.proxy.rlwy.net',  # Use the public proxy host
        'PORT': '47804',  # Use the public proxy port
    }
}

DATABASE_ROUTERS = ['app.routers.BigQueryRouter']

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For collected static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # For your static files
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # For production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development
EMAIL_HOST = os.getenv('EMAIL_HOST', 'your-smtp-server')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your-email@example.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-password')

# Additional allauth settings
ACCOUNT_EMAIL_VERIFICATION = 'none'  # or 'optional' or 'none'
LOGIN_REDIRECT_URL = '/admin/'  # Change from '/admin/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'  # Change from '/admin/'
LOGIN_URL = '/accounts/login/'  # Add this line to specify the login URL

UNFOLD = {
    "SITE_TITLE": "Leadzz",
    "SITE_HEADER": "Leadzz",
    "SIDEBAR": {
        "navigation": [
            {
                "items": [
                    {
                        "title": _("Contact Lists"),
                        "icon": "list",
                        "link": "/admin/app/contactlist/",
                        "permission": lambda request: request.user.has_perm('app.view_contactlist'),
                    },
                    {
                        "title": _("Contacts"),
                        "icon": "person",
                        "link": "/admin/app/contact/",
                        "permission": lambda request: request.user.has_perm('app.view_contact'),
                    },
                ],
            },
            {
                "title": _("Administration"),
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": "/admin/auth/user/",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}

CSRF_TRUSTED_ORIGINS = [
    'https://leadzz-production.up.railway.app',
]