# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def send_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps({'notification': notification}))
