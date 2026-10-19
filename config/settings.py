"""
Django settings for config project (Pozicky Predlznikov).
"""

import os
from pathlib import Path

import dj_database_url
from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-tr7k-l6xn_cmnc57v31&15k%be%15*-@wp0itf32f58c^twb$9',
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=Csv(),
)

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://www.pozickypredlznikov.sk,https://pozickypredlznikov.sk',
    cast=Csv(),
)
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'users',
    'auctions',
    'bids',
    'designs',
    'adminpanel',
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
    'users.middleware.ImpersonateMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.impersonation',
                'core.context_processors.notifications',
                'adminpanel.context_processors.admin_badges',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# Custom user model
AUTH_USER_MODEL = 'users.User'

#: Vlastný backend navyše odmieta prihlásenie pre účty zablokované administrátorom.
AUTHENTICATION_BACKENDS = [
    'users.backends.BlockAwareModelBackend',
]


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'sk'

TIME_ZONE = 'Europe/Bratislava'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads, e.g. KYC docs) - local for now, swap for S3-like storage later
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#: Neutrálna rozlišovacia stránka - investor aj dlžník majú vlastné prihlásenie
#: (users:login_investor / users:login_borrower), users:login je len pre admina.
LOGIN_URL = 'core:landing'
LOGIN_REDIRECT_URL = 'core:landing'
LOGOUT_REDIRECT_URL = 'core:landing'


# E-mailové notifikácie
# V DEBUG móde (lokálny vývoj) sa e-maily len vypíšu do konzoly. Na produkcii
# treba nastaviť SMTP_HOST/SMTP_USER/SMTP_PASSWORD (napr. SendGrid, Mailgun,
# Gmail SMTP) cez premenné prostredia v Render dashboarde - kód je pripravený,
# stačí doplniť prístupové údaje, nič sa v kóde meniť nemusí.
SMTP_HOST = config('SMTP_HOST', default='')
if SMTP_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = SMTP_HOST
    EMAIL_PORT = config('SMTP_PORT', default=587, cast=int)
    EMAIL_HOST_USER = config('SMTP_USER', default='')
    EMAIL_HOST_PASSWORD = config('SMTP_PASSWORD', default='')
    EMAIL_USE_TLS = config('SMTP_USE_TLS', default=True, cast=bool)
else:
    # Bez nastaveného SMTP sa e-maily vypisujú do logu/konzoly - appka funguje
    # ďalej bez chyby, len reálne e-maily neodosiela.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Pôžičky pre Dlžníkov <noreply@pozickypredlznikov.sk>')


# Security (relevant behind Render's proxy / HTTPS)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
