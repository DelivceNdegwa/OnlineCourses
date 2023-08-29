from celery import shared_task
from time import sleep
from courses.models import Video
from courses.selectors import get_specific_video
from courses.notifications import send_notification

@shared_task
def generate_dash_files(video_id):
    print("--Generating DASH--")
    video = get_specific_video({'id': video_id})
    status_message = "Processing the video"
    success_message ="Video processing complete"
    failed_message = "Video processing failed"
    if not video:
        print("-------------------No video-------------------")
        send_notification(video_id, failed_message, success=False)
        raise Exception(f"No video with the ID {video_id}, please provide a valid video")

    if video.dash_manifest:
        return True
    
    try:
        print(f"-------------------{status_message}-------------------")
        send_notification(video_id, status_message, success=False)
        video.generate_dash()
        # Call the send_notification function when dash generation is complete
        send_notification(video_id, success_message, success=True)
    except Exception as e:
        send_notification(video_id, failed_message, success=False)
        raise f"--Something went wrong--\n{e}"