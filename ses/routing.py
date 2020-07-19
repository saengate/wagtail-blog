from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(
        r'^ws/testing/$',
        consumers.SESConsumer,
        name='projetc',
    ),
]
