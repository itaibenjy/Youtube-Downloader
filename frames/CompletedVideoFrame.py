import customtkinter
from pytube import Stream
from PIL import Image
import os
import subprocess
from common.HelpTip import HelpTip
from common.AssetsController import DownloadAssets
from downloads.DownloadManager import DownloadManager
from urllib.request import urlopen
import bordercrop

TITLE_LENGTH = 60
HOVER_COLOR = ("gray70", "gray30");

class CompletedVideoFrame(customtkinter.CTkFrame):
    def __init__(self, downloadPages, master, stream_data: dict):
        super().__init__(master)

        self.stream_data = stream_data

        self.downloadPages = downloadPages

        self.columnconfigure(1, weight = 1)


        try:
            self.thumbnail = customtkinter.CTkImage(bordercrop.crop(stream_data["thumbnail"], MINIMUM_ROWS=10), size=(160,90))
        except ValueError:
            self.thumbnail = customtkinter.CTkImage(Image.open(urlopen(stream_data["thumbnail"])), size=(120, 90))

        self.file_path = stream_data["file_path"]

        self.assets =  DownloadAssets()

        # image
        self.thumbnail_image = customtkinter.CTkLabel(self, text="", image=self.thumbnail)
        self.thumbnail_image.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="nswe")
        
        # title
        title = stream_data["title"] if len(stream_data["title"]) <= TITLE_LENGTH else stream_data["title"][:TITLE_LENGTH] + "..."
        self.title_label = customtkinter.CTkLabel(self, text=title, font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=1, column=1, columnspan=2, padx=10, pady=(10,5), sticky="nsw")
        HelpTip(master, self.title_label, message=stream_data["title"])

        # details
        self.video_details_label = customtkinter.CTkLabel(self, text=stream_data["details"],
                                                          font=customtkinter.CTkFont(size=12))
        self.video_details_label.grid(row=2, column=1, columnspan=2, padx=10, pady=(0,10), sticky="nsw")

        # file size
        self.file_size = customtkinter.CTkLabel(self, text=f"{round(stream_data['file_size'], 1)}MB")
        self.file_size.grid(row=3, column=1, padx=10, pady=10, sticky="nsw")

        # open button
        self.open_button = customtkinter.CTkButton(self, text="Open", command=self.open_file)
        self.open_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10, sticky="nsw")

        # delete button
        self.delete_button = customtkinter.CTkButton(self, text="", fg_color = "transparent", hover_color=HOVER_COLOR,width=15, command=self.delete_file, anchor="center", image=self.assets.delete_icon)
        self.delete_button.grid(row=1, column=3, padx=10, pady=10, sticky="e")

    
    def open_file(self):
        try:
            os.startfile(self.file_path)
        except AttributeError:
            subprocess.call(['open', self.file_path])

    def delete_file(self):
        DownloadManager.delete_download(self.stream_data)
        self.downloadPages.remove_element((self.stream_data))
        print("delete")
