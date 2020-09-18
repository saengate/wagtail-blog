from django.middleware.csrf import CsrfViewMiddleware
from wagtail.core.views import serve
from blog.models.contactpage import ContactPage

import logging

logger = logging.getLogger(__name__)


class ContactCsrfViewMiddleware(CsrfViewMiddleware):

    def process_view(self, request, callback, callback_args, callback_kwargs):

        if callback == serve:
            # We are visiting a wagtail page. Check if this is a ContactPage
            # and if so, do not perfom any CSRF validation
            page = ContactPage.objects.first()
            path = callback_args[0]

            if page and path.startswith(page.get_url_parts()[-1][1:]):
                return self._accept(request)

        return super().process_view(request, callback, callback_args, callback_kwargs)
