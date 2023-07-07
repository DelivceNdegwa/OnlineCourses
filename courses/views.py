from django.shortcuts import render, get_object_or_404
from .models import Video



def video_stream(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    dash_manifest_url = video.generate_dash()

    return render(request, 'courses/video.html', {'dash_manifest_url': dash_manifest_url})

