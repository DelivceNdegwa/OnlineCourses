import logging
from celery import shared_task
from courses.selectors import get_specific_video
from courses.notifications import send_notification
from courses.models import VideoDocument

logger = logging.getLogger(__name__)


@shared_task
def generate_dash_files(video_id):
    logger.info("--Generating DASH--")
    video = get_specific_video({'id': video_id})
    status_message = "Processing the video"
    success_message ="Video processing complete"
    failed_message = "Video processing failed"
    if not video:
        logger.error("-------------------No video-------------------")
        send_notification(video_id, failed_message, success=False)
        raise Exception(f"No video with the ID {video_id}, please provide a valid video")

    if video.dash_manifest:
        return True
    
    try:
        logger.info(f"-------------------{status_message}-------------------")
        send_notification(video_id, status_message, success=False)
        video.generate_dash()
        # Call the send_notification function when dash generation is complete
        video_document = VideoDocument.objects.filter(video=video).first()
        video_document.is_ready = True
        video_document.save()
        send_notification(video_id, success_message, success=True)
    except Exception as e:
        logger.error("--Something went wrong--\n{e}")
        send_notification(video_id, failed_message, success=False)
        raise f"--Something went wrong--\n{e}"