import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save

# from b2b_downloads.apps.scrape.models import DownloadHistory
# from b2b_downloads.apps.scrape.serializers import DownloadHistorySignalSerializer


logger = logging.getLogger(__name__)


# @receiver(post_save, sender=DownloadHistory)
# def websocket_broadcast_updated_client(sender, instance=None, **kwargs):
#     serializer = DownloadHistorySignalSerializer(instance)
#     channel_layer = get_channel_layer()
#     data = {
#         'type': 'model_update',
#         'model': sender.__name__,
#         'instance': serializer.data,
#     }
#     async_to_sync(channel_layer.group_send)('b2bdownload', data)
