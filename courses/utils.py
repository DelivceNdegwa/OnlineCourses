import os
import subprocess
from django.core.files.storage import default_storage
from . import constants

class VideoProcessor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, video_instance):
        self.video_instance = video_instance

    def process(self, protocol):
        if protocol == constants.DASH:
            self.process_dash()
        elif protocol == constants.HLS:
            self.process_hls()

    def process_dash(self):
        output_dir = self.get_output_directory(constants.DASH)
        
        print(f"CHEKIIII::::{self.manifest_exists(output_dir, constants.DASH)}")
        if self.manifest_exists(output_dir, constants.DASH):
            return 

        self.preprocess_video(output_dir, constants.DASH)

    def process_hls(self):
        output_dir = self.get_output_directory(constants.HLS)
        if self.manifest_exists(output_dir, constants.HLS):
            return

        self.preprocess_video(output_dir, constants.HLS)

    def manifest_exists(self, output_dir, protocol):
        manifest_path = os.path.join(output_dir, self.get_manifest_filename(protocol))
        return default_storage.exists(manifest_path)

    def get_output_directory(self, protocol):
        return f'media/{protocol}/{self.video_instance.pk}'

    def get_manifest_filename(self, protocol):
        if protocol == constants.DASH:
            return 'manifest.mpd'
        elif protocol == constants.HLS:
            return 'index.m3u8'

    def preprocess_video(self, output_dir, protocol):
        os.makedirs(output_dir, exist_ok=True)

        segment_duration = 5

        common_cmd = [
            "ffmpeg",
            "-i", self.video_instance.video_file.path,
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "veryfast",
            "-c:a", "aac",
            "-b:a", "128k",
        ]
        hls_cmd = [
            "-hls_time", str(segment_duration),
            "-hls_playlist_type", "vod",
            "-hls_segment_type", "mpegts",
            "-hls_segment_filename", f"{output_dir}/segment_%d.ts",
            f"{output_dir}/{self.get_manifest_filename(constants.HLS)}"
        ]

        dash_cmd = [
            "-f", "dash",
            "-seg_duration", str(segment_duration),
            f"{output_dir}/{self.get_manifest_filename(constants.DASH)}"
        ]

        cmd = common_cmd + (hls_cmd if protocol == constants.HLS else dash_cmd)

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print("FFmpeg command failed with error:", e)
            print("FFmpeg command:", " ".join(cmd))
            raise e

        manifest_path = os.path.join(output_dir, self.get_manifest_filename(protocol))
        if protocol == constants.HLS:
            self.video_instance.hls_manifest.name = manifest_path
        elif protocol == constants.DASH:
            self.video_instance.dash_manifest.name = manifest_path
        self.video_instance.save()
