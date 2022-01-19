from tkinter import *

import processing_functions


class Interface:
    window = None
    label_title = None
    label_link = None
    label_complete = None
    label_already_exists = None
    link = None
    entry_link = None
    button_mp3 = None
    button_mp4 = None

    # initializer for variables in interface
    @classmethod
    def __init__(cls):
        # initialize Processor class, else it will return None
        processing_functions.Processor.__init__()

        # window root
        cls.window = Tk()

        # labels
        cls.label_title = Label(cls.window,
                                text='YouTube Video Downloader',
                                font='calibri 20 bold')
        cls.label_link = Label(cls.window,
                               text='Enter Your Link:',
                               font='calibri 17 bold')
        cls.label_complete = Label(cls.window,
                                   text='Download Complete!',
                                   font='arial 15')
        cls.label_already_exists = Label(cls.window,
                                         text='The file already exists.',
                                         font='arial 15')

        # entry
        cls.link = StringVar()  # text for entry
        cls.entry_link = Entry(cls.window,
                               width=40,
                               textvariable=cls.link,
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

    @classmethod
    def message_complete(cls):
        cls.forget_all_messages()
        cls.label_complete.place(x=160, y=230)

    @classmethod
    def message_already_exists(cls):
        cls.forget_all_messages()
        cls.label_already_exists.place(x=155, y=230)

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
    def get_link(cls):
        return cls.link

    # on application start
    @classmethod
    def open_application(cls):
        # window attributes
        cls.window.geometry('500x300')
        cls.window.resizable(0, 0)  # (width, height)
        cls.window.title("YTB VD")

        # label attributes
        cls.label_title.pack()
        cls.label_link.place(x=173, y=50)

        # entry attributes
        cls.entry_link.place(x=28, y=90)

        # button attributes
        cls.button_mp3.place(x=50, y=130)
        cls.button_mp4.place(x=270, y=130)

        # loop window
        cls.window.mainloop()
