import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)


class SesConfig(AppConfig):
    name = 'ses'

    def ready(self):
        logger.info('SESConfig app loaded')
        import signals  # NOQA
