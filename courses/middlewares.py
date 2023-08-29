# your_app/middlewares.py
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session



User = get_user_model()


@database_sync_to_async
def get_user(query_string):
    try:
        session_key = parse_qs(query_string.decode('utf-8'))['session_key'][0]
        session = Session.objects.get(session_key=session_key)
        return session.get_decoded().get('_auth_user_id')
    except (Session.DoesNotExist, KeyError):
        return None

class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").split(b"&")
        user_id = await get_user(query_string)
        
        if user_id is None:
            scope['user'] = AnonymousUser()
        else:
            scope['user'] = await self.get_user(user_id)

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
