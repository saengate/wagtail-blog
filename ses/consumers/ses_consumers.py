import logging
import json

from datetime import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


logger = logging.getLogger(__name__)


class SESConsumer(WebsocketConsumer):
    GROUP_NAME = 'generic'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME,
            self.channel_name,
        )

    def ses_message(self, event):
        self.send(text_data=event['message'])

    def receive(self, text_data=None):
        dt = datetime.now()
        text_data = {
            'type': 'ses.message',
            'message': f'Conectado al websocket el {dt}',
        }
        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            text_data,
        )

    def model_update(self, event):
        logger.info(f"Sending data update.")
        text_data = {
            'type': 'ses.message',
            'message': json.dumps(event),
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            self.GROUP_NAME,
            text_data,
        )
