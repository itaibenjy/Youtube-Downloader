import customtkinter
from pytube import Stream
from PIL import Image
import os
import subprocess
from common.HelpTip import HelpTip
from common.AssetsController import DownloadAssets
from downloads.DownloadManager import DownloadManager
from common.YouTubeHelper import YouTubeHelper
from dialogs.AlertDialog import AlertDialog

TITLE_LENGTH = 60
HOVER_COLOR = ("gray70", "gray30");

class CompletedVideoFrame(customtkinter.CTkFrame):
    def __init__(self, downloadPages, stream_data: dict):
        super().__init__(downloadPages)

        self.stream_data = stream_data

        self.downloadPages = downloadPages

        self.columnconfigure(1, weight = 1)

        # checking if the stream file exists in the download path 
        if not os.path.isfile(stream_data["file_path"]):
            stream_data["details"] = "FILE NOT FOUND!"


        self.thumbnail = customtkinter.CTkImage(YouTubeHelper.get_cropped_thumbnail(stream_data["thumbnail"]), size=(160,90))

        self.file_path = stream_data["file_path"]

        self.assets =  DownloadAssets()

        # image
        self.thumbnail_image = customtkinter.CTkLabel(self, text="", image=self.thumbnail)
        self.thumbnail_image.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="nswe")
        
        # title
        title = stream_data["title"] if len(stream_data["title"]) <= TITLE_LENGTH else stream_data["title"][:TITLE_LENGTH] + "..."
        self.title_label = customtkinter.CTkLabel(self, text=title, font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=1, column=1, columnspan=2, padx=10, pady=(10,5), sticky="nsw")
        HelpTip(downloadPages, self.title_label, message=stream_data["title"])

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
        self.delete_button = customtkinter.CTkButton(self, text="", fg_color = "transparent", hover_color=HOVER_COLOR,width=15, command=self.delete_event, anchor="center", image=self.assets.delete_icon)
        self.delete_button.grid(row=1, column=3, padx=10, pady=10, sticky="e")
        HelpTip(downloadPages, self.delete_button, message="Delete file")

        self.dialog = None

    
    def open_file(self):
        try:
            os.startfile(self.file_path)
        except AttributeError:
            subprocess.call(['open', self.file_path])
    
    def delete_event(self):
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = AlertDialog(self.delete_file, "You are about to delete a file", "You are about to delete this file:\n"+ f"{self.stream_data['title']}\n" + self.stream_data["details"]) 
        else:
            self.dialog.focus()
        

    def delete_file(self):
        DownloadManager.delete_download(self.stream_data)
        self.downloadPages.remove_element((self.stream_data))
