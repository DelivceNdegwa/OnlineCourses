# your_notifications_module.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from courses import selectors

channel_layer = get_channel_layer()

def send_notification(video_id, message):
    video = selectors.get_specific_video({'id': video_id})
    video.processing_state = 'complete'
    video.save()

    notification = f"Video uploading and processing complete for video ({video_id}): {message}"

    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'notification': notification,
        }
    )