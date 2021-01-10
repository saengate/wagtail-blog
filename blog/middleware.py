import logging
import os

from django.middleware.csrf import CsrfViewMiddleware
from wagtail.core.views import serve
from blog.models.contactpage import ContactPage


logger = logging.getLogger(__name__)


class ContactCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):

        if callback == serve:
            # We are visiting a wagtail page. Check if this is a ContactPage
            # and if so, do not perfom any CSRF validation
            page = ContactPage.objects.first().get_url_parts()[-1][1:]
            environment = os.environ.get('ENV', 'local')
            path = callback_args[0]

            if environment == 'production':
                path = f'production/{path}'

            if page and path.startswith(page):
                return self._accept(request)

        return super().process_view(request, callback, callback_args, callback_kwargs)
