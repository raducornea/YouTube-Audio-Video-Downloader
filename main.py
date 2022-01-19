# 1. Add libraries
import os
from tkinter import *
import moviepy.editor as mp
from pytube import YouTube
from pathlib import Path


downloads_path = str(Path.home() / "Downloads")


# https://www.youtube.com/watch?v=Q7PZFT3msPE&ab_channel=light%27sslowed
# https://www.youtube.com/watch?v=BaB0e3O08I4
def combine_audio(video_name, audio_name, out_name):

    clip = mp.VideoFileClip(video_name).subclip()
    clip.write_videofile(out_name, audio=audio_name)


# 4. Download Function
def downloader_mp3():
    url = YouTube(str(link.get()))  # get link string and puts it in url

    # video = url.streams.filter(only_audio=True).first()  # filters video only by audio and mp3
    audio = url.streams.get_audio_only()

    # before downloading, check if it exists already. if so -> do nothing
    title = audio.title
    current_audio_path = os.getcwd()
    possible_existing_mp3 = current_audio_path + '\\' + title + '.mp3'

    if os.path.isfile(downloads_path + '\\' + title + '.mp3'):
        message_already_exists()
    else:
        possible_existing_mp4 = current_audio_path + '\\' + str(url.title) + '.mp4'
        if os.path.isfile(possible_existing_mp4):
            os.rename(possible_existing_mp4,
                      current_audio_path + '\\' + 'pleasedonotnameyourfileslikethisjpxproasdf.mp4')
            process_audio(url, current_audio_path)
            os.rename(current_audio_path + '\\' + 'pleasedonotnameyourfileslikethisjpxproasdf.mp4',
                      possible_existing_mp4)
        else:
            process_audio(url, current_audio_path)
        os.replace(possible_existing_mp3, downloads_path + '\\' + title + '.mp3')

        message_complete()


def process_audio(url, current_audio_path):
    out_file = url.streams.filter(mime_type='audio/mp4').first().download(output_path=current_audio_path)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)


def downloader_mp4():
    url = YouTube(str(link.get()))

    title = str(url.title) + '.mp4'

    current_video_path = os.getcwd()
    possible_existing_mp4 = current_video_path + '\\' + title
    if os.path.isfile(downloads_path + '\\' + title + '.mp4'):
        message_already_exists()
    else:
        # before downloading, check if mp3 exists already
        possible_existing_mp3 = current_video_path + '\\' + str(url.title) + '.mp3'
        if os.path.isfile(downloads_path + '\\' + title + '.mp3'):
            # a) it does -> combine it without removing it
            process_video(url, possible_existing_mp4, current_video_path, title)
        else:
            # b) it doesn't -> download it, combine it, then remove it
            downloader_mp3()
            process_video(url, possible_existing_mp4, current_video_path, title)
            os.remove(possible_existing_mp3)
        os.replace(possible_existing_mp4, downloads_path + '\\' + title + '.mp4')

        message_complete()


def process_video(url, possible_existing_mp4, current_video_path, title):
    video = url.streams.filter(mime_type='video/mp4').order_by('resolution').desc().first()
    video.download(output_path=current_video_path)

    print(video.title)
    combine_audio(video.title + '.mp4', video.title + '.mp3', 'pleasedonotnameyourfileslikethisjpxproasdf.mp4')
    os.remove(possible_existing_mp4)
    os.rename(current_video_path + '\\' + 'pleasedonotnameyourfileslikethisjpxproasdf.mp4',
              current_video_path + '\\' + title)


def message_complete():
    Label(window, text='                        ', font='arial 15').place(x=155, y=230)
    Label(window, text='Download Complete!      ', font='arial 15').place(x=160, y=230)


def message_already_exists():
    Label(window, text='                        ', font='arial 15').place(x=155, y=230)
    Label(window, text='The file already exists.', font='arial 15').place(x=155, y=230)


if __name__ == '__main__':
    # 2. Create Display Window
    window = Tk()  # makes a widget
    window.geometry('500x300')  # sets geometry of the widget
    window.resizable(0, 0)  # resizable in width x height
    window.title("YTB VD")  # sets name to widget

    Label(window, text='YouTube Video Downloader', font='calibri 20 bold').pack()  # can't be modified by users

    # 3. Create Field to Enter Link
    link = StringVar()  # string variable to enter in the text box
    link_enter = Entry(window, width=40, textvariable=link, font='arial 15 italic').place(x=28, y=90)
    Label(window, text='Enter Your Link:', font='calibri 17 bold').place(x=173, y=50)

    # Entry - input text
    # window = widget name
    # width = how long the text box is
    # text variable = the text on the width
    # x = where does it start in width  # y = where does it start in height

    # 4. Download Function Button
    Button(window, text='DOWNLOAD MP3', font='arial 15 bold', bg='yellow',
           pady=20, command=downloader_mp3).place(x=50, y=130)
    Button(window, text='DOWNLOAD MP4', font='arial 15 bold', bg='yellow',
           pady=20, command=downloader_mp4).place(x=270, y=130)

    # command = what function to execute when it is pressed

    # 5. Run the program
    window.mainloop()
