from celery import shared_task
from time import sleep
from courses.models import Video

@shared_task
def generate_dash_files(video):
    if type(video) is not Video:
        raise Exception("Please provide a valid video")

    if video.dash_manifest:
        return True
    
    try:
        video.generate_dash()
    except Exception as e:
        raise f"--Something went wrong--\n{e}"