import django
from django.core.asgi import get_asgi_application

django.setup()

from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import (
    AllowedHostsOriginValidator
)
from chats.tokenauth_middleware import TokenAuthMiddleware
from chats.chats_routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    )
})
