import customtkinter
from pytube import Stream
from PIL import Image
import os
import subprocess

class CompletedVideoFrame(customtkinter.CTkFrame):
    def __init__(self, master, stream:Stream, thumbnail:Image, file_path:str):
        super().__init__(master)
        self.columnconfigure(1, weight = 1)

        self.thumbnail = thumbnail
        self.stream = stream
        self.file_path = file_path
        """
        if stream.type == "video":
            self.file_path=os.path.join(file_path, f"{stream.title.replace(' ','')}_{stream.resolution}_{stream.fps}fps.{stream.subtype}")
        else:
            self.file_path=os.path.join(file_path, f"{stream.title.replace(' ','')}_{stream.abr}.{stream.subtype}")
            """

        # image
        self.thumbnail_image = customtkinter.CTkLabel(self, text="", image=thumbnail)
        self.thumbnail_image.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="nswe")
        
        # title
        self.title_label = customtkinter.CTkLabel(self, text=stream.title, font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=1, column=1, columnspan=2, padx=10, pady=(10,5), sticky="nsw")

        # details
        if(stream.type == "video"):
            type = "Video" if stream.is_progressive else "Video Only"
            self.video_details_label = customtkinter.CTkLabel(self, text=f"{type}  ·  {stream.resolution}  ·  {stream.subtype}  ·  {stream.fps}FPS",
                                                          font=customtkinter.CTkFont(size=12))
        else:
            type = "Audio Only"
            self.video_details_label = customtkinter.CTkLabel(self, text=f"{type}  ·  {stream.subtype}  · {stream.abr}",
                                                          font=customtkinter.CTkFont(size=12))
        self.video_details_label.grid(row=2, column=1, columnspan=2, padx=10, pady=(0,10), sticky="nsw")

        # progress_bar
        self.file_size = customtkinter.CTkLabel(self, text=f"{stream.filesize_mb}MB")
        self.file_size.grid(row=3, column=1, padx=10, pady=10, sticky="nsw")

        # precentage
        self.open_button = customtkinter.CTkButton(self, text="Open", command=self.open_file)
        self.open_button.grid(row=3, column=2, padx=10, pady=10, sticky="nsw")

    
    def open_file(self):
        try:
            os.startfile(self.file_path)
        except AttributeError:
            subprocess.call(['open', self.file_path])
