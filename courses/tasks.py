from celery import shared_task
from time import sleep
from courses.models import Video
from courses.selectors import get_specific_video

@shared_task
def generate_dash_files(video_id):
    video = get_specific_video({'id': video_id})
    if not video:
        raise Exception(f"No video with the ID {video_id}, please provide a valid video")

    if video.dash_manifest:
        return True
    
    try:
        video.generate_dash()
    except Exception as e:
        raise f"--Something went wrong--\n{e}"