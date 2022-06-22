from tkinter import *
from tkinter import filedialog

import processing_functions


class Interface:
    window = None
    label_title = None
    label_link = None
    label_complete = None
    label_already_exists = None
    link = None
    path = None
    entry_link = None
    entry_path = None
    button_mp3 = None
    button_mp4 = None
    button_browse = None
    label_path = None
    #todo
    #  read absolute_path from a file and place it if it's null in the entry at the beginning
    absolute_path = None

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

    @classmethod
    def download_mp3(cls):
        processing_functions.Processor.downloader_mp3()

    @classmethod
    def download_mp4(cls):
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

    @classmethod
    def get_link(cls):
        return cls.link

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
