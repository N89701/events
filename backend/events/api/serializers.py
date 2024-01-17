from asyncio import run

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import (
    ModelSerializer, IntegerField, ImageField
)

from tables.models import Organization, Event
from .sleep import sleep_endpoint

User = get_user_model()


class UserCustomSerializer(UserCreateSerializer):
    """Сериализатор для создания и полного отображения пользователя."""

    id = IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'organization',
            'phone_number'
        )


class ShortUserSerializer(UserCustomSerializer):
    """Сериализатор для отображения пользователя в организации."""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
        )


class OrganizationSerializer(ModelSerializer):
    """Сериализер для создания и отображения организации."""

    id = IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id',
            'title',
            'description',
            'address',
            'postcode'
        )


class OrganizationInEventSerializer(ModelSerializer):
    """Сериализер для отображения организации в мероприятии."""
    employee = ShortUserSerializer(many=True)

    class Meta:
        model = Organization
        fields = (
            'id',
            'title',
            'employee',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['address'] = f"{instance.address}, {instance.postcode}"
        return data


class EventGetSerializer(ModelSerializer):
    """Сериализер для отображения мероприятий."""

    id = IntegerField(read_only=True)
    organizations = OrganizationInEventSerializer(many=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'organizations',
            'image',
            'date'
        )


class EventCreateSerializer(ModelSerializer):
    """Сериализер для создания мероприятий."""

    id = IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'organizations',
            'image',
            'date'
        )

    def create(self, validated_data):
        run(sleep_endpoint())
        return super().create(validated_data)
