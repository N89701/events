from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Chat, Message

User = get_user_model()


class UserChatAndMessageSerializer(UserSerializer):
    """Сериализатор для отображения пользователя в чатах и сообщениях."""

    class Meta:
        ordering = ['id']
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class ChatReadSerializer(serializers.ModelSerializer):
    """Сериализатор для метода get для чатов."""

    initiator = UserChatAndMessageSerializer(read_only=True)
    receiver = UserChatAndMessageSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'initiator', 'receiver', 'last_message')

    def get_last_message(self, obj) -> str:
        last_message = obj.messages.order_by('-pub_date').first()
        if last_message:
            return last_message.text
        return ''


class ChatCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания чата."""

    class Meta:
        model = Chat
        fields = ('receiver',)

    def validate(self, data):
        initiator = self.context.get('request').user
        receiver = data.get('receiver')
        if initiator == receiver:
            raise ValidationError('Нельзя создавать чат с самим собой.')
        if Chat.objects.filter(
            initiator=initiator,
            receiver=receiver
        ).exists():
            raise ValidationError(
                detail='Чат уже существует.'
            )
        if Chat.objects.filter(
            initiator=receiver,
            receiver=initiator
        ).exists():
            raise ValidationError(
                detail='Чат уже существует.'
            )
        data['initiator'] = initiator
        return data

    def to_representation(self, instance):
        serializer = ChatReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщения."""

    sender = UserChatAndMessageSerializer(read_only=True)
    chat = ChatReadSerializer(read_only=True)
    receiver = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = Message
        fields = (
            'id', 'chat', 'sender', 'receiver', 'text', 'pub_date',
        )

    def create(self, validated_data):
        validated_data.pop('receiver', None)
        return super().create(validated_data)
