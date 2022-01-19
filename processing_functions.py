import os

import moviepy.editor as mp
from pytube import YouTube
from pathlib import Path

import user_interface


class Processor:
    downloads_path = None

    @classmethod
    def __init__(cls):
        cls.downloads_path = str(Path.home()/"Downloads")

    @classmethod
    def combine_audio(cls, video_name, audio_name, out_name):
        clip = mp.VideoFileClip(video_name).subclip()
        clip.write_videofile(out_name, audio=audio_name)

    @classmethod
    def process_audio(cls, url, current_audio_path):
        out_file = url.streams.filter(mime_type='audio/mp4').first().download(output_path=current_audio_path)
        # base, ext = os.path.splitext(out_file)
        # new_file = f"{base}.mp3"
        # os.rename(out_file, new_file)

    @classmethod
    def process_video(cls, url, possible_existing_mp4, current_video_path, title):
        video = url.streams.filter(mime_type='video/mp4').order_by('resolution').desc().first()
        video.download(output_path=current_video_path)

        print(video.title)
        cls.combine_audio(video.title + '.mp4', video.title + '.mp3', 'pleasedonotnameyourfileslikethisjpxproasdf.mp4')
        os.remove(possible_existing_mp4)
        os.rename(current_video_path + '\\' + 'pleasedonotnameyourfileslikethisjpxproasdf.mp4',
                  current_video_path + '\\' + title)

    @classmethod
    def downloader_mp3(cls):
        link = str(user_interface.Interface.get_link().get())
        url = YouTube(link)

        # video = url.streams.filter(only_audio=True).first()  # filters video only by audio and mp3
        audio = url.streams.get_audio_only()

        # before downloading, check if it exists already. if so -> do nothing
        title = audio.title
        current_audio_path = os.getcwd()
        possible_existing_mp3 = f"{current_audio_path}\\{title}.mp3"

        cls.process_audio(url, current_audio_path)
        user_interface.Interface.message_complete()

    @classmethod
    def downloader_mp4(cls):
        link = user_interface.Interface.get_link()
        url = YouTube(str(link.get()))

        title = str(url.title) + '.mp4'

        current_video_path = os.getcwd()
        possible_existing_mp4 = f"{current_video_path}\\{title}"
        if os.path.isfile(f"{cls.downloads_path}\\{title}.mp4"):
            user_interface.Interface.message_already_exists()
        else:
            # before downloading, check if mp3 exists already
            possible_existing_mp3 = current_video_path + '\\' + str(url.title) + '.mp3'
            if os.path.isfile(cls.downloads_path + '\\' + title + '.mp3'):
                # a) it does -> combine it without removing it
                cls.process_video(url, possible_existing_mp4, current_video_path, title)
            else:
                # b) it doesn't -> download it, combine it, then remove it
                cls.downloader_mp3()
                cls.process_video(url, possible_existing_mp4, current_video_path, title)
                os.remove(possible_existing_mp3)
            os.replace(possible_existing_mp4, cls.downloads_path + '\\' + title + '.mp4')

            user_interface.Interface.message_complete()
