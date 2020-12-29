import os

from config.core_settings import *  # NOQA

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Refer to secret from project Secrets usually PROJECTNAME_SECRET

SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = INSTALLED_APPS + [  # NOQA
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.frontend_cache',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.api.v2',

    # https://docs.coderedcorp.com/wagtail-cache/stable/getting_started/install.html
    'wagtailcache',

    'home',
    'search',
    'blog',
]

MIDDLEWARE = MIDDLEWARE + [  # NOQA
    'wagtailcache.cache.UpdateCacheMiddleware',
    'blog.middleware.ContactCsrfViewMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'wagtailcache.cache.FetchFromCacheMiddleware',
]

REST_FRAMEWORK.update(  # NOQA
    {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PARSER_CLASSES': [
            'rest_framework.parsers.JSONParser',
        ],
    }
)

# This is the human-readable name of your Wagtail install
# which welcomes users upon login to the Wagtail admin.
WAGTAIL_SITE_NAME = 'Blog SaenGate'

# Override the search results template for wagtailsearch
# WAGTAILSEARCH_RESULTS_TEMPLATE = 'myapp/search_results.html'
# WAGTAILSEARCH_RESULTS_TEMPLATE_AJAX = 'myapp/includes/search_listing.html'

# Replace the search backend
# WAGTAILSEARCH_BACKENDS = {
#  'default': {
#    'BACKEND': 'wagtail.search.backends.elasticsearch2',
#    'INDEX': 'myapp'
#  }
# }

# Wagtail email notifications from address
# WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'wagtail@myhost.io'

# Wagtail email notification format
# WAGTAILADMIN_NOTIFICATION_USE_HTML = True

WAGTAILIMAGES_FORMAT_CONVERSIONS = {
    'bmp': 'jpeg',
}

# Reverse the default case-sensitive handling of tags
TAGGIT_CASE_INSENSITIVE = True

WAGTAILAPI_USE_FRONTENDCACHE = True
REDIS_HOST = os.getenv('REDIS_HOST', 'redis://redis:6379')
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_SUBJECT_PREFIX = '[Blog SaenGate] '

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
EMAIL_PORT = 587

EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'saengatehost@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
