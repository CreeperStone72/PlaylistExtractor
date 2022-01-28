import os
import re

import moviepy.editor as mp
from pytube import YouTube, Playlist
from tkinter import Label


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
