"""
ASGI config for online_courses project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_courses.settings')
http_config = {
    "http": get_asgi_application(),
}
application = ProtocolTypeRouter(http_config)
