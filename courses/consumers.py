# your_app/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            await self.accept()
            await self.channel_layer.group_add("notifications", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({'notification': notification}))
