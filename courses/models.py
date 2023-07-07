from django.db import models
from . import constants
from .utils import VideoProcessor

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    hls_manifest = models.FileField(upload_to='hls/', blank=True, null=True)
    dash_manifest = models.FileField(upload_to='dash/', blank=True, null=True)
    
    def generate_hls(self):
        video_processor = VideoProcessor(self)
        video_processor.process(constants.HLS)
        return self.hls_manifest.url
    
    def generate_dash(self):
        video_processor = VideoProcessor(self)
        video_processor.process(constants.DASH)
        return self.dash_manifest.url
    
    def __str__(self):
        return f"{self.title}:{self.video_file}"