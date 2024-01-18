from datetime import datetime

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .pagination import LimitPageNumberPagination
from .permissions import UserCustomPermission
from .serializers import (
    Event, EventCreateSerializer, EventGetSerializer, Organization,
    OrganizationSerializer
)


class OrganizationViewSet(ModelViewSet):
    """Вьюсет для работы с организациями."""
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (UserCustomPermission,)
    pagination_class = LimitPageNumberPagination


class EventViewSet(ModelViewSet):
    """Вьюсет для работы с мероприятиями."""
    queryset = Event.objects.all()
    serializer_class = EventGetSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title',)
    ordering = ('date', '-date')

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return EventCreateSerializer
        return EventGetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        date_later = self.request.query_params.get('date>')
        date_earlier = self.request.query_params.get('date<')
        if date_later:
            date = datetime.strptime(date_later, '%d/%m/%Y %H.%M')
            queryset = queryset.filter(date__gt=date)
        if date_earlier:
            date = datetime.strptime(date_earlier, '%d/%m/%Y %H.%M')
            queryset = queryset.filter(date__lt=date)
        return queryset
