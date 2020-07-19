import logging

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from rest_framework import (
    serializers,
    permissions,
    viewsets,
)
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from ses import msgs
from utils.translation import translate as t


logger = logging.getLogger(__name__)


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    language_native = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('__all__')

    def get_language(self, obj):
        request = self.context['request']
        _t = t(request, msgs.I.TEST_TEXT)
        msg = _t['msg']
        self.context['request'] = _t['request']
        return f"Debe verse en el lenguaje del usuario: {msg}"

    def get_language_native(self, obj):
        return f"Debe verse en el lenguaje del settings: {msgs.I.TEST_TEXT}"


class UserView(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    @permission_classes((permissions.AllowAny,))
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(
            queryset,
            many=True,
            context={'request': request},
        )
        logger.info(_(f"Debe verse en el lenguaje del settings: {msgs.I.TEST_LOG}"))
        return Response(serializer.data)
