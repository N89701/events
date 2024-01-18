from django.db import models

from tables.models import User

class Chat(models.Model):
    """Модель чата."""

    initiator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats_initiator',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats_receiver',
    )

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['initiator', 'receiver'],
                name='selfchatting_forbidden'
            ),
        ]


class Message(models.Model):
    """Модель сообщения."""

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='message_sender',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
