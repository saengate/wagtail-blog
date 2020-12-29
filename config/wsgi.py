"""
WSGI config for mysite django.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
project_folder = os.path.expanduser('/webapps/wagtailblog')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


environment = os.environ.get('ENV', 'local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings.' + environment)
application = get_wsgi_application()
