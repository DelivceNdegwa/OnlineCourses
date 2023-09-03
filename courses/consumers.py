# your_app/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging


logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"----CONSUMER SEND NOTIFICATION CALLED: connect initializing----")
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)
        
        # if self.scope['user'].is_anonymous:
        #     await self.close()
        # else:
        #     await self.accept()
        #     await self.channel_layer.group_add("notifications", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    async def send_notification(self, event):
        notification = event['notification']
        logger.info(f"----CONSUMER SEND NOTIFICATION CALLED: {notification}----")
        await self.send(text_data=json.dumps({'notification': notification}))
