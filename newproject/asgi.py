import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import register.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            register.routing.websocket_urlpatterns
        )
    ),
})