import datetime

from django.db.models import Max, Q
from django.db.models.functions import Coalesce
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from api.permissions import IsInitiatorOrReceiverChatPermission
from .models import Chat
from .serializers import ChatCreateSerializer, ChatReadSerializer


class ChatViewSet(viewsets.ModelViewSet):
    """
    Вью для работы с чатами.
    Также позволяет получать чат по ID.

    """

    http_method_names = ['get', 'post']
    permission_classes = [
        IsAuthenticated,
        IsInitiatorOrReceiverChatPermission
    ]
    pagination_class = LimitPageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        try:
            chat = self.get_object()
        except Http404:
            return Response(
                {"detail": "Чат не найден."},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user not in (chat.initiator, chat.receiver):
            return Response(
                {"detail": "Вы не можете просматривать детали этого чата."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        null_date = datetime.datetime.min
        return Chat.objects.filter(
            Q(initiator=user) | Q(receiver=user)
        ).annotate(
            last_message_date=Coalesce(Max('messages__pub_date'), null_date)
        ).order_by('-last_message_date', '-id')

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return ChatCreateSerializer
        return ChatReadSerializer

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)
