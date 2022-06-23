import os
from tkinter import *
from tkinter import filedialog
import re
import processing_functions


class Interface:
    window = None
    label_title = None
    label_link = None
    label_complete = None
    label_already_exists = None
    label_path_corrupted = None
    label_link_corrupted = None
    link = None
    path = None
    entry_link = None
    entry_path = None
    button_mp3 = None
    button_mp4 = None
    button_browse = None
    label_path = None

    # initializer for variables in interface
    @classmethod
    def __init__(cls):
        # initialize Processor class, else it will return None
        processing_functions.Processor.__init__()

        # window root
        cls.window = Tk()

        # labels
        cls.label_link = Label(cls.window,
                               text='Enter Your Link:',
                               font='calibri 17 bold')
        cls.label_path = Label(cls.window,
                               text='Enter Your Path or Browse it:',
                               font='calibri 17 bold')
        cls.label_complete = Label(cls.window,
                                   text='Download Complete!',
                                   font='arial 15')
        cls.label_already_exists = Label(cls.window,
                                         text='The file already exists.',
                                         font='arial 15')
        cls.label_path_corrupted = Label(cls.window,
                                         text='Choose a valid path!',
                                         font='arial 15')
        cls.label_link_corrupted = Label(cls.window,
                                         text='Choose a valid link!',
                                         font='arial 15')

        # entries
        cls.link = StringVar()  # text for entry
        cls.entry_link = Entry(cls.window,
                               width=40,
                               textvariable=cls.link,
                               font='arial 15 italic')
        cls.path = StringVar()
        cls.entry_path = Entry(cls.window,
                               width=33,
                               textvariable=cls.path,
                               font='arial 15 italic')

        # buttons
        cls.button_mp3 = Button(cls.window,
                                text='DOWNLOAD MP3',
                                font='arial 15 bold',
                                bg='yellow',
                                pady=20,
                                command=cls.download_mp3)
        cls.button_mp4 = Button(cls.window,
                                text='DOWNLOAD MP4',
                                font='arial 15 bold',
                                bg='yellow',
                                pady=20,
                                command=cls.download_mp4)
        cls.button_browse = Button(cls.window,
                                   text='Browse',
                                   font='arial 12 bold',
                                   bg='light grey',
                                   pady=1,
                                   command=cls.browse)

        with open(f"{processing_functions.Processor.project_path}\\path.txt", "r+") as path_file:
            line = path_file.readlines()[0]
            if line != "":
                cls.write_entry_path(line)
                processing_functions.Processor.set_path(line)

    @classmethod
    def message_complete(cls):
        cls.forget_all_messages()
        cls.label_complete.place(x=160, y=195)

    @classmethod
    def message_already_exists(cls):
        cls.forget_all_messages()
        cls.label_already_exists.place(x=155, y=195)

    @classmethod
    def forget_all_messages(cls):
        cls.label_complete.place_forget()
        cls.label_already_exists.place_forget()
        cls.label_link_corrupted.place_forget()
        cls.label_path_corrupted.place_forget()

    @classmethod
    def entry_cheks(cls):
        entry_path = cls.entry_path.get()
        entry_link = cls.entry_link.get()

        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_match = re.match(youtube_regex, entry_link)
        if not youtube_regex_match:
            cls.forget_all_messages()
            cls.label_link_corrupted.place(x=160, y=195)
            return False

        if not os.path.exists(entry_path):
            cls.forget_all_messages()
            cls.label_path_corrupted.place(x=160, y=195)
            return False

        return True

    @classmethod
    def download_mp3(cls):
        if cls.entry_cheks():
            processing_functions.Processor.downloader_mp3()

    @classmethod
    def download_mp4(cls):
        if cls.entry_cheks():
            processing_functions.Processor.downloader_mp4()

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

    # on application start
    @classmethod
    def open_application(cls):
        # window attributes
        cls.window.geometry('500x350')
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

        # loop window
        cls.window.mainloop()
