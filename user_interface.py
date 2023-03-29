import json
from tkinter import *
from tkinter import filedialog, ttk
from playsound import playsound

import os
import re

from pytube import Playlist

import processing_functions
from threading import *
import queue


class Interface:
    window = None
    background_application_color = None
    background_entry_color = None
    background_button_download_color = None
    background_button_browse_color = None
    background_label_color = None
    text_application_color = None
    text_entry_color = None
    text_button_download_color = None
    text_button_browse_color = None
    text_label_color = None
    label_title = None
    label_link = None
    label_complete = None
    label_already_exists = None
    label_path_corrupted = None
    label_link_corrupted = None
    label_progress_bar = None
    label_download_thread_already_running = None
    link = None
    path = None
    entry_link = None
    entry_path = None
    button_mp3 = None
    button_mp4 = None
    button_browse = None
    progress_bar = None
    label_path = None
    download_thread = None
    progress_bar_queue = None
    active_thread_progress_bar = None
    progress_bar_thread = None
    option_to_print = None
    choice = None
    old_value = 0
    links_to_process = []

    # initializer for variables in interface
    @classmethod
    def __init__(cls):
        # initialize Processor class, else it will return None
        processing_functions.Processor.__init__()

        # colors
        with open("colors.json", "r+") as json_file:
            data = json.load(json_file)
            cls.background_application_color = data.get("background_application_color")
            cls.background_entry_color = data.get("background_entry_color")
            cls.background_button_download_color = data.get("background_button_download_color")
            cls.background_button_browse_color = data.get("background_button_browse_color")
            cls.background_label_color = data.get("background_label_color")
            cls.text_application_color = data.get("text_application_color")
            cls.text_entry_color = data.get("text_entry_color")
            cls.text_button_download_color = data.get("text_button_download_color")
            cls.text_button_browse_color = data.get("text_button_browse_color")
            cls.text_label_color = data.get("text_label_color")

        # window root
        cls.window = Tk()
        cls.window.configure(background=cls.background_application_color)

        # labels
        cls.label_link = Label(cls.window,
                               text='Enter your link:',
                               bg=cls.background_label_color,
                               fg=cls.text_label_color,
                               font='calibri 17 bold')
        cls.label_path = Label(cls.window,
                               text='Enter your path or browse it:',
                               bg=cls.background_label_color,
                               fg=cls.text_label_color,
                               font='calibri 17 bold')
        cls.label_complete = Label(cls.window,
                                   text='Download Complete!',
                                   bg=cls.background_label_color,
                                   fg=cls.text_label_color,
                                   font='arial 15')
        cls.label_already_exists = Label(cls.window,
                                         text='The file already exists.',
                                         bg=cls.background_label_color,
                                         fg=cls.text_label_color,
                                         font='arial 15')
        cls.label_path_corrupted = Label(cls.window,
                                         text='Choose a valid path!',
                                         bg=cls.background_label_color,
                                         fg=cls.text_label_color,
                                         font='arial 15')
        cls.label_link_corrupted = Label(cls.window,
                                         text='Choose a valid link!',
                                         bg=cls.background_label_color,
                                         fg=cls.text_label_color,
                                         font='arial 15')
        cls.label_progress_bar = Label(cls.window,
                                       text='Progress... ',
                                       bg=cls.background_label_color,
                                       fg=cls.text_label_color,
                                       font='arial 15')
        cls.label_download_thread_already_running = Label(cls.window,
                                                          text='Please wait all operations to finish!',
                                                          bg=cls.background_label_color,
                                                          fg=cls.text_label_color,
                                                          font='arial 15')

        # entries
        cls.link = StringVar()  # text for entry
        cls.entry_link = Entry(cls.window,
                               width=40,
                               bg=cls.background_entry_color,
                               fg=cls.text_entry_color,
                               textvariable=cls.link,
                               font='arial 15 italic')
        cls.path = StringVar()
        cls.entry_path = Entry(cls.window,
                               width=33,
                               bg=cls.background_entry_color,
                               fg=cls.text_entry_color,
                               textvariable=cls.path,
                               font='arial 15 italic')

        # buttons
        cls.button_mp3 = Button(cls.window,
                                text='DOWNLOAD MP3',
                                font='arial 15 bold',
                                bg=cls.background_button_download_color,
                                fg=cls.text_button_download_color,
                                pady=20,
                                command=cls.download_mp3)
        cls.button_mp4 = Button(cls.window,
                                text='DOWNLOAD MP4',
                                font='arial 15 bold',
                                bg=cls.background_button_download_color,
                                fg=cls.text_button_download_color,
                                pady=20,
                                command=cls.download_mp4)
        cls.button_browse = Button(cls.window,
                                   text='Browse',
                                   font='arial 12 bold',
                                   bg=cls.background_button_browse_color,
                                   fg=cls.text_button_browse_color,
                                   pady=1,
                                   command=cls.browse)
        cls.progress_bar = ttk.Progressbar(
            cls.window,
            orient='horizontal',
            mode='determinate',
            length=445
        )

        cls.progress_bar_queue = queue.Queue()
        cls.active_thread_progress_bar = True
        cls.progress_bar_thread = Thread(target=cls.listen_progressbar_messages)
        cls.progress_bar_thread.start()

        with open(f"{processing_functions.Processor.project_path}\\path.txt", "r+") as path_file:
            line = path_file.readlines()[0]
            if line != "":
                cls.write_entry_path(line)
                processing_functions.Processor.set_path(line)

        cls.option_to_print = "Audio"
        cls.choice = "Audio"
        cls.links_to_process = []

        cls.old_value = 0

    @classmethod
    def listen_progressbar_messages(cls):
        # must stop it when closing the app via cls.active_queue = False
        while cls.active_thread_progress_bar:
            message = cls.progress_bar_queue.get()

            if message == "Close":
                cls.active_thread_progress_bar = False
            else:
                cls.progress_bar['value'] = float(message)
                cls.label_progress_bar = Label(cls.window,
                                               text=f"{cls.option_to_print}: {round(float(message), 2)} %       ",
                                               bg=cls.background_label_color,
                                               fg=cls.text_label_color,
                                               font='arial 15')
                cls.label_progress_bar.place(x=180, y=390)
                pass

    @classmethod
    def message_complete(cls):
        cls.forget_all_messages()
        cls.label_complete.place(x=160, y=195)
        cls.label_progress_bar = Label(cls.window,
                                       text=f"{cls.option_to_print}: 100.0 %       ",
                                       bg=cls.background_label_color,
                                       fg=cls.text_label_color,
                                       font='arial 15')
        cls.label_progress_bar.place(x=180, y=390)

    @classmethod
    def message_already_exists(cls):
        cls.forget_all_messages()
        cls.label_already_exists.place(x=155, y=195)
        cls.enable_everything_again()

    @classmethod
    def message_download_thread_already_running(cls):
        cls.forget_all_messages()
        cls.label_download_thread_already_running.place(x=100, y=195)

    @classmethod
    def forget_all_messages(cls):
        cls.label_complete.place_forget()
        cls.label_already_exists.place_forget()
        cls.label_link_corrupted.place_forget()
        cls.label_path_corrupted.place_forget()
        cls.label_download_thread_already_running.place_forget()
        cls.label_progress_bar.place_forget()
        cls.progress_bar['value'] = 0  # trebuie pus ca sa ramana pe interfata...

    @classmethod
    def entry_cheks(cls):
        entry_path = cls.entry_path.get()
        entry_link = cls.entry_link.get()

        youtube_regex_playlist = (r'^.*(youtu.be\/|list=)([^#\&\?]*).*')
        youtube_regex_playlist_match = re.match(youtube_regex_playlist, entry_link)
        youtube_regex_link = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_link_match = re.match(youtube_regex_link, entry_link)

        print(youtube_regex_link_match)
        print(youtube_regex_playlist_match)
        if not youtube_regex_link_match and not youtube_regex_playlist_match:
            cls.forget_all_messages()
            cls.label_link_corrupted.place(x=160, y=195)
            return False

        if not os.path.exists(entry_path) or entry_path == "":
            cls.forget_all_messages()
            cls.label_path_corrupted.place(x=160, y=195)
            return False

        return True

    @classmethod
    def play_click_sounds(cls):
        sound_thread = Thread(target=playsound, args=("sounds/mixkit-clear-mouse-clicks-2997.wav",))
        sound_thread.start()

    @classmethod
    def get_links_list(cls):
        link = str(cls.get_link())

        youtube_regex_playlist = (r'^.*(youtu.be\/|list=)([^#\&\?]*).*')
        youtube_regex_playlist_match = re.match(youtube_regex_playlist, link)

        youtube_regex_link = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_link_match = re.match(youtube_regex_link, link)

        # if is a playlist, but there's a video playing in the link, not a list of videos
        links = []
        if "index" in link or (not youtube_regex_playlist_match and youtube_regex_link_match):
            links.append(link)
        else:
            try:
                playlist = Playlist(link)
                links = playlist.video_urls
            except:
                links.append(link)

        return list(links)

    @classmethod
    def download_mp3(cls):
        # cls.play_click_sounds()
        cls.option_to_print = "Audio"
        if cls.download_thread is not None and cls.download_thread.is_alive():
            cls.message_download_thread_already_running()
        elif cls.entry_cheks():
            cls.links_to_process = cls.get_links_list()

            # normal operations
            cls.choice = "Audio"
            cls.forget_all_messages()
            cls.disable_while_downloading()
            cls.download_thread = Thread(target=processing_functions.Processor.downloader_mp3)
            cls.download_thread.start()
            cls.progress_bar_queue.put(0)

    @classmethod
    def download_mp4(cls):
        # cls.play_click_sounds()
        cls.option_to_print = "Video"
        if cls.download_thread is not None and cls.download_thread.is_alive():
            cls.message_download_thread_already_running()
        if cls.entry_cheks():
            cls.links_to_process = cls.get_links_list()

            cls.choice = "Video"
            cls.forget_all_messages()
            cls.disable_while_downloading()
            cls.download_thread = Thread(target=processing_functions.Processor.downloader_mp4)
            cls.download_thread.start()
            cls.progress_bar_queue.put(0)

    @classmethod
    def disable_while_downloading(cls):
        cls.button_mp3["state"] = "disabled"
        cls.button_mp4["state"] = "disabled"
        cls.button_browse["state"] = "disabled"
        cls.entry_path.config(state="disabled")
        cls.entry_link.config(state="disabled")

    @classmethod
    def enable_everything_again(cls):
        cls.button_mp3["state"] = "normal"
        cls.button_mp4["state"] = "normal"
        cls.button_browse["state"] = "normal"
        cls.entry_path.config(state="normal")
        cls.entry_link.config(state="normal")

    @classmethod
    def browse(cls):
        folder_selected = filedialog.askdirectory()
        print(folder_selected)

        if folder_selected != "":
            processing_functions.Processor.set_path(folder_selected)
            cls.write_entry_path(folder_selected)

    @classmethod
    def write_entry_path(cls, text):
        cls.entry_path.delete(0, END)
        cls.entry_path.insert(0, text)

        with open(f"{processing_functions.Processor.project_path}\\path.txt", "r+") as path_file:
            path_file.seek(0)
            path_file.truncate()
            path_file.write(text)

    @classmethod
    def get_link(cls):
        return cls.link.get()

    @classmethod
    def on_closing(cls):
        cls.progress_bar_queue.put("Close")
        cls.window.destroy()

    # on application start
    @classmethod
    def open_application(cls):
        # window attributes
        cls.window.geometry('500x450')
        cls.window.resizable(0, 0)  # (width, height)
        cls.window.title("YouTube Video Downloader")

        # label attributes
        cls.label_link.place(x=25, y=30)
        cls.label_path.place(x=25, y=120)

        # entry attributes
        cls.entry_link.place(x=28, y=70)
        cls.entry_path.place(x=28, y=160)

        # button attributes
        cls.button_mp3.place(x=50, y=230)
        cls.button_mp4.place(x=270, y=230)
        cls.button_browse.place(x=400, y=156)

        cls.progress_bar.place(x=28, y=350)

        # add close event handler
        cls.window.protocol("WM_DELETE_WINDOW", cls.on_closing)

        # loop window
        cls.window.mainloop()
