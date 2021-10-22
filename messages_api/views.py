from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import exception_handler

from authz.permissions import HasAdminPermission
from messages_api.models import Message
from messages_api.serializers import MessageSerializer


class MessageApiView(RetrieveAPIView):
    serializer_class = MessageSerializer
    message = None

    def get_object(self):
        return Message(message=self.message)


class PublicMessageApiView(MessageApiView):
    message = "The API doesn't require an access token to share this message."


class AuthMessageApiView(MessageApiView):
    message = "The API successfully validated your access token."
    permission_classes = [IsAuthenticated]


class AdminMessageApiView(MessageApiView):
    message = "The API successfully recognized you as an admin."
    permission_classes = [IsAuthenticated, HasAdminPermission]


def api_exception_handler(exc, context=None):
    response = exception_handler(exc, context=context)
    if response and isinstance(response.data, dict):
        response.data = {'message': response.data.get('detail', 'API Error')}
    else:
        response.data = {'message': 'API Error'}
    return response
