import pygments

from config.settings.base import *  # NOQA
from os import getenv
from utils.color_logging import formatter

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENVIRONMENT = 'develop'

HOSTS = {
    'production': ['127.0.0.1'],
    'develop': ['127.0.0.1', '0.0.0.0', 'localhost'],
}

WS_ALLOWED_HOSTS = ['*'] if DEBUG else HOSTS[ENVIRONMENT]

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wagtaildb',
        'USER': 'userdb',
        'PASSWORD': 'password',
        'HOST': 'wagtail-db',
        'PORT': '5432',
    },
}

INSTALLED_APPS += [  # NOQA
    'zappa_django_utils',
]

# ==============================================================================
# WEBSOCKETS & CHANNELS
# ==============================================================================

REDIS_HOST = getenv('REDIS_HOST', 'redis://redis:6379')

# It is possible to have multiple channel layers configured.
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_HOST],
        },
    },
}


WAGTAILAPI_USE_FRONTENDCACHE = True
WAGTAILAPI_BASE_URL = 'http://0.0.0.0:7000'

# WAGTAIL_CACHE_BACKEND = 'pagecache'
CACHES = {
    'default': {
        'BACKEND': 'wagtailcache.compat_backends.django_redis.RedisCache',
        'LOCATION': REDIS_HOST,
        'KEY_PREFIX': 'wagtailcache',
        'TIMEOUT': 3600,  # one hour (in seconds)
    },
}

# INIT CONFIG WAGTAIL-COMPOSE
WAGTAILFRONTENDCACHE = {
    'redis': {
        'BACKEND': 'wagtailcache.compat_backends.django_redis.RedisCache',
        'LOCATION': REDIS_HOST,
    },
}

ADMINS = [
    ('Saúl Galán', 'saengate@gmail.com'),
]
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Blog SaenGate] '

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

# CORS_ORIGIN_WHITELIST = [
#     "http://localhost:7000",
#     "http://127.0.0.1:7000"
# ]

# END CONFIG WAGTAIL-COMPOSE

# https://django-extensions.readthedocs.io/en/latest/shell_plus.html
# ./manage.py shell_plus --notebook
# Always use IPython for shell_plus
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
# Truncate sql queries to this number of characters (this is the default)
SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000
# To disable truncation of sql queries use
SHELL_PLUS_PRINT_SQL_TRUNCATE = None
# Specify sqlparse configuration options when printing sql queries to the console
SHELL_PLUS_SQLPARSE_FORMAT_KWARGS = dict(
    reindent_aligned=True,
    truncate_strings=500,
)

# Specify Pygments formatter and configuration options when printing sql queries to the console
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}

# Additional IPython arguments to use
IPYTHON_ARGUMENTS = [
    '--ext', 'django_extensions.management.notebook_extension',
    '--debug',
]

IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"
# Additional Notebook arguments to use
NOTEBOOK_ARGUMENTS = []
NOTEBOOK_KERNEL_SPEC_NAMES = ["python3", "python"]

NOTEBOOK_ARGUMENTS = [
    '--allow-root',
    '--ip', '0.0.0.0',
    '--port', '7001',
]

# LOGS
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': formatter(),
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'console': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'all': {
            'class': 'utils.color_logging.NewLogger',
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# CORS config https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True

# To allow default credentials
CORS_ALLOW_CREDENTIALS = True
