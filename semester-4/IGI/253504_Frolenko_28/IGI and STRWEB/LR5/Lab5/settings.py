import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1a4lcln-o22lz&d^0k@7@t9ydlw$t08y8bhg9*r8vb33$!f_+c'

LOGGING_LEVEL = os.getenv('DJANGO_LOGGING_LEVEL', 'DEBUG').upper()

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'Lab5',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': 'django_debug.log',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOGGING_LEVEL,
            'propagate': True,
        },
    },
}



LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'Lab5.CustomUser'

ROOT_URLCONF = 'Lab5.urls'

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'Lab5.context_processors.current_time'
            ],
        },
    },
]

WSGI_APPLICATION = 'Lab5.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

GEOIP_PATH = '/path/to/geoip'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
