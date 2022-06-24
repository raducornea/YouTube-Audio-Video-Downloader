from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from pathlib import Path

import user_interface
import shutil
import os


class Processor:
    downloads_path = None
    project_path = None

    @classmethod
    def __init__(cls):
        cls.downloads_path = str(Path.home() / "Downloads")
        cls.project_path = os.getcwd()

    @classmethod
    def set_path(cls, path):
        cls.downloads_path = path

    @classmethod
    # change format to mp3
    def process_audio(cls, title):
        os.chdir(cls.project_path)
        clip = AudioFileClip(f"{title}.mp4")

        os.chdir(cls.downloads_path)
        clip.write_audiofile(f"{title}.mp3")
        clip.close()

        user_interface.Interface.message_complete()

    @classmethod
    def downloader_mp3(cls):
        link = str(user_interface.Interface.get_link())
        url = YouTube(link)

        audio = url.streams.get_audio_only()
        title = audio.title

        mp3_path = f"{cls.downloads_path}\\{title}.mp3"
        mp4_path = f"{cls.project_path}\\{title}.mp4"
        if os.path.exists(mp3_path):
            user_interface.Interface.message_already_exists()
            return

        url.streams.filter(mime_type='audio/mp4').first().download(output_path=cls.project_path)
        cls.process_audio(title)
        os.remove(mp4_path)

    @classmethod
    def combine_audio(cls, video_name, audio_name, out_name):
        clip = VideoFileClip(video_name).subclip()
        clip.write_videofile(out_name, audio=audio_name)

    @classmethod
    def process_video(cls, url):
        video = url.streams.filter(mime_type='video/mp4').order_by('resolution').desc().first()
        video.download(output_path=cls.project_path)

        mp4_clip = f"{video.title}.mp4"
        mp3_clip = f"{video.title}.mp3"
        final_clip = f"{video.title}_auxiliary.mp4"
        cls.combine_audio(mp4_clip, mp3_clip, final_clip)

        source = cls.project_path + '\\' + final_clip
        destination = cls.downloads_path + '\\' + mp4_clip
        shutil.move(source, destination)

        os.remove(cls.project_path + '\\' + mp4_clip)

    @classmethod
    def downloader_mp4(cls):
        link = user_interface.Interface.get_link()
        url = YouTube(str(link))
        title = str(url.title)

        mp3_path = f"{cls.project_path}\\{title}.mp3"
        mp4_path = f"{cls.downloads_path}\\{title}.mp4"
        if os.path.exists(mp4_path):
            user_interface.Interface.message_already_exists()
            return

        # trick the program to download the mp3 in project
        actual_download_path = cls.downloads_path
        cls.set_path(cls.project_path)
        cls.downloader_mp3()

        # set os path back to normal
        cls.set_path(actual_download_path)
        cls.process_video(url)
        os.remove(mp3_path)

        user_interface.Interface.message_complete()
