from pathlib import Path
import os

import django.utils.log
from dotenv import load_dotenv
import logging


logger = logging.getLogger(__name__)


# Загрузка переменных среды из файла .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',
    'django_filters',
    'articles',
    'authorization',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_apscheduler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'news_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {'signup': 'authorization.models.BasicSignupForm'}

LOGIN_URL = '/accounts/login/' #!!!!!
LOGIN_REDIRECT_URL = '/news/' #!!!!!!

WSGI_APPLICATION = 'news_portal.wsgi.application'

SITE_ID = 1
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'esmirasar'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо писать user, иными словами, это всё то что идёт до собаки
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER + '@yandex.ru'

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'format_console_debug': {
            'format': '{asctime} {levelname}: {message}',
            'datefmt': '%d-%m-%Y %H:%M',
            'style': '{',
        },
        'format_console_warning': {
            'format': '{pathname}: {asctime} {levelname}: {message}',
            'datefmt': '%d-%m-%Y %H:%M',
            'style': '{',
        },
        'format_console_error': {
            'format': '{pathname}: {asctime} {levelname}: {message} {exc_info}',
            'datefmt': '%d-%m-%Y %H:%M',
            'style': '{',
        },
        'format_general_log': {
            'format': '{asctime} {levelname}: {module} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        }
    },
    'filters': {
        'filter_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'filter_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console_debug': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'format_console_debug',
            'filters': ['filter_debug_true', ]
        },
        'console_warning': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'format_console_warning',
            'filters': ['filter_debug_true', ]
        },
        'console_error': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'formatter': 'format_console_error',
            'filters': ['filter_debug_true', ]
        },
        'general_log_info': {
            'class': 'logging.FileHandler',
            'filename': 'Logs/general.log',
            'level': 'INFO',
            'formatter': 'format_general_log',
            'filters': ['filter_debug_false', ]
        },
        'errors_log': {
            'class': 'logging.FileHandler',
            'filename': 'Logs/errors.log',
            'level': 'ERROR',
            'formatter': 'format_console_error',
        },
        'security_log': {
            'class': 'logging.FileHandler',
            'filename': 'Logs/security.log',
            'level': 'INFO',
            'formatter': 'format_general_log'
        },
        'send_mail': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'formatter': 'format_console_warning',
            'filters': ['filter_debug_false', ]
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug',
                         'console_warning',
                         'console_error',
                         'general_log_info', ],
            'propagate': True
        },
        'django.request': {
            'handlers': ['errors_log',
                         'send_mail', ],
            'propagate': True
        },
        'django.server': {
            'handlers': ['errors_log',
                         'send_mail', ],
            'propagate': True
        },
        'django.template': {
            'handlers': ['errors_log', ],
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['errors_log', ],
            'propagate': True
        },
        'django.security': {
            'handlers': ['security_log', ],
            'propagate': False
        },
    }
}
