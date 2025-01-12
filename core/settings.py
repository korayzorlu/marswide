"""
Django settings for marswide_backend project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

from decouple import config, Csv

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast = bool, default = False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast = Csv(), default = "*,www.marswide.com,marswide.com")


# Application definition

INSTALLED_APPS = [
    "daphne",
    "clearcache",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    "rest_framework",
    "rest_framework_datatables_editor",
    "drf_multiple_model",
    "django_filters",
    "django_cleanup.apps.CleanupConfig",
    "corsheaders",
    "simple_history",
    "django_ckeditor_5",
    "django_celery_results",
    "django_celery_beat",
    "django_select2",
    "crispy_forms",
    "crispy_bootstrap5",
    "users",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

#WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'
CHANNEL_LAYERS= {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("db", 6380)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

USE_RDS = config('USE_RDS', cast = bool, default = False)

if USE_RDS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            #'ENGINE': 'django_postgrespool2',
            'NAME': 'postgres',
            'USER': 'micho',
            'PASSWORD': 'Novu.23.PG!',
            'HOST': 'micho-app-db.czrnghcpuvme.eu-central-1.rds.amazonaws.com',
            'PORT': os.getenv("PG_PORT",""),
            "TEST": {
                "NAME": "postgres",
            },
        }
    }
else:
    DATABASES = {
            'default': {
                'ENGINE': 'dj_db_conn_pool.backends.postgresql',
                'NAME': str(os.getenv('PG_DB')),
                'USER': str(os.getenv('PG_USER')),
                'PASSWORD': str(os.getenv('PG_PASSWORD')),
                'HOST': 'db',
                'PORT': '',
                'POOL_OPTIONS': {
                    'POOL_SIZE': 100,
                    'MAX_OVERFLOW': 50,
                    'RECYCLE': 300
                },
                #'CONN_MAX_AGE': 30, # Bağlantı ömrü (saniye cinsinden)
                "TEST": {
                    "NAME": "marswidedb_test",
                },
            }
    }


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

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

SECURE_BROWSER_XSS_FILTER = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

USE_S3 = config('USE_S3', cast = bool, default = False)

if USE_S3:
    AWS_ACCESS_KEY_ID=str(os.getenv('AWS_ACCESS_KEY_ID'))
    AWS_SECRET_ACCESS_KEY=str(os.getenv('AWS_SECRET_ACCESS_KEY'))
    AWS_STORAGE_BUCKET_NAME="michoapp-bucket"
    AWS_S3_REGION_NAME= 'eu-central-1'
    AWS_DEFAULT_ACL= None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    DEFAULT_FILE_STORAGE= 'core.settings.s3utils.PublicMediaStorage'
    STATICFILES_STORAGE= 'core.settings.s3utils.StaticStorage'
    
    STATIC_LOCATION = 'static'
    PUBLIC_MEDIA_LOCATION= "media"
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
else:
    STATIC_URL = "/staticfiles/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect



# Rest Framework

REST_FRAMEWORK = {
    # 'DATE_INPUT_FORMATS': "%d %b %Y",
    'DATE_FORMAT': "%d.%m.%Y",
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework_datatables.filters.DatatablesFilterBackend',
        'rest_framework_datatables_editor.filters.DatatablesFilterBackend'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
        'rest_framework_datatables_editor.renderers.DatatablesRenderer'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables_editor.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 200,
}


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Celery

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//' # Rabbitmq için
#CELERY_BROKER_URL = 'redis://redis:6379/0' # Redis için

CELERY_TIMEZONE = "Europe/Istanbul"
#CELERY_TASK_TRACK_STARTED = True
#CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# Proxy

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Caches

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'qr-code': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'qr-code-cache',
        'TIMEOUT': 3600
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis:db:6380/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles-filehashes'
    }
}

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "{levelname} - {asctime} - {module} - {process:d} - {thread:d} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
            "formatter": "verbose",
            "when" : "midnight",
            "interval" : 1,
            "backupCount" : 7,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        'channels': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Maintenance

MAINTENANCE_MODE = config('MAINTENANCE_MODE', cast = bool, default = False)

# Cors for react
CORS_ALLOW_CREDENTIALS = True
#CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if os.getenv("CORS_ALLOWED_ORIGINS", "") else []

CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if os.getenv("CSRF_TRUSTED_ORIGINS", "") else []

SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE")  # veya 'Lax' ya da 'Strict'
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE")



# CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True
# CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']

# Ckeditor

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # Kullanılacak araç çubuğu
        'height': 300,
        'width': '100%',
        'removePlugins': 'stylesheetparser',  # İstenmeyen özellikleri kaldırabilirsiniz
        'extraPlugins': 'codesnippet',  # Ek özellikler ekleyebilirsiniz
    },
}

# Select2

SELECT2_CACHE_BACKEND = "select2"

# Iframe

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Template

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Access

os.environ['IP'] = str(os.getenv('IP'))