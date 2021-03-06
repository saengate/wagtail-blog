from config.settings.base import *  # NOQA
from os import getenv

ENVIRONMENT = 'production'

HOSTS = ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".execute-api.us-east-1.amazonaws.com",
    ".saengate.com",
    ".cloudfront.net",
]

INSTALLED_APPS = INSTALLED_APPS + [  # NOQA
    'django_s3_storage',
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('DATABASE_NAME'),
        'USER': getenv('DATABASE_USER'),
        'PASSWORD': getenv('DATABASE_PASSWORD'),
        'HOST': getenv('DATABASE_HOST'),
        'PORT': getenv('DATABASE_PORT'),
    },
}

WAGTAILAPI_BASE_URL = 'www.saengate.com'

ADMINS = [
    ('Saúl Galán', 'saengate@gmail.com'),
]
MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

# CORS config https://pypi.org/project/django-cors-headers/
# CORS_ALLOWED_ORIGIN_REGEXES = (r'^(.*)?\.saengate\.com$', )
CORS_ORIGIN_ALLOW_ALL = True

# Django-S3-Storage in settings
YOUR_S3_BUCKET = "staticfiles-saengate-blog"

AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET
STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
AWS_STORAGE_BUCKET_NAME = YOUR_S3_BUCKET

# These next two lines will serve the static files directly
# from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
AWS_S3_MAX_AGE_SECONDS_STATIC = "94608000"
