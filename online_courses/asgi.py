"""
ASGI config for online_courses project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from courses.routing import websocket_urlpatterns
from courses.middlewares import WebSocketAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_courses.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": AuthMiddlewareStack(
        WebSocketAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
