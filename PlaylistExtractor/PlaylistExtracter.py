import os
import re
from tkinter import Label
from tkinter import Tk, Entry, Button, filedialog

import moviepy.editor as mp
from pytube import YouTube, Playlist


class PlaylistConvert:
    def __init__(self, link: str, folder: str, status: Label):
        self.playlist = Playlist(link)
        self.folder = folder
        self.status = status

    def bulk_download(self):
        self.download_playlist()
        print(self.folder)
        self.mp4_to_mp3()

    def download_playlist(self):
        for url in self.playlist:
            self.set_status(f'Downloading {url}...')
            YouTube(url).streams.filter(only_audio=True).first().download(output_path=self.folder)
            self.set_status('Finished')
        self.set_status('Playlist downloaded. Starting conversion')

    def mp4_to_mp3(self):
        print(os.listdir(self.folder))
        for file in os.listdir(self.folder):
            self.set_status(file)
            if re.search('mp4', file):
                mp4_path = os.path.join(self.folder, file)
                mp3_path = os.path.join(self.folder, os.path.splitext(file)[0]+'.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)
        self.set_status('Conversion finished. Enjoy your music')

    def set_status(self, message: str):
        self.status.configure(text=message)


class UIFrame(object):
    def __init__(self, title: str, width: int, height: int, padding: int):
        self.frame = Tk()
        self.frame.geometry(f'{width}x{height}')
        self.frame.title(title)
        self.frame.resizable(width=False, height=False)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.destination = os.path.join(os.getcwd(), 'songs')

        # Creating the widgets
        label_title = Label(self.frame, text="Youtube playlist downloader", font=("Arial", 15))
        label_playlist = Label(self.frame, text="Link to the playlist")
        label_destination = Label(self.frame, text="Destination path")

        self.entry_playlist = Entry(self.frame, width=width)
        self.label_destination = Label(self.frame, text=self.get_destination(), width=(width - padding))
        button_file = Button(self.frame, text="🔍", width=padding, command=self.find_destination)

        button_submit = Button(self.frame, text="Download", width=width, command=self.submit)

        self.label_status = Label(self.frame, text="Enter the link, pick your destination and hit Download")

        # Placing the widgets
        label_title.grid(row=0, columnspan=2)

        self.frame.rowconfigure(1, weight=1)

        label_playlist.grid(row=2, columnspan=2, padx=padding)
        self.entry_playlist.grid(row=3, columnspan=2, padx=padding)

        self.frame.rowconfigure(4, weight=1)

        label_destination.grid(row=5, columnspan=2, padx=padding)
        self.label_destination.grid(row=6, column=0, padx=padding)
        button_file.grid(row=6, column=1, padx=padding)

        self.frame.rowconfigure(7, weight=1)

        button_submit.grid(row=8, columnspan=2, padx=padding)

        self.frame.rowconfigure(9, weight=1)

        self.label_status.grid(row=10, columnspan=2, padx=padding)

        # Starting the window
        self.frame.mainloop()

    def get_link(self) -> str:
        return self.entry_playlist.get()

    def get_destination(self) -> str:
        return self.destination

    def find_destination(self):
        filename = filedialog.askdirectory(initialdir=os.getcwd(), title="Pick your destination", mustexist=True)
        self.label_destination.configure(text=filename)
        self.destination = filename

    def submit(self):
        print(self.get_link())
        print(self.get_destination())

        converter = PlaylistConvert(self.get_link(), self.get_destination(), self.label_status)
        converter.bulk_download()


UIFrame("Playlist extractor", 500, 200, 5)
