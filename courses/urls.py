from django.urls import path
from . import views


app_name="courses"
urlpatterns = [
    path('video/<video_id>', views.video_stream, name="video_stream")
]
