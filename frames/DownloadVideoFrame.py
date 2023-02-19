import customtkinter
from pytube import Stream
from PIL import Image
from common.YouTubeHelper import YouTubeHelper

class DownloadVideoFrame(customtkinter.CTkFrame):
    def __init__(self, master, stream:Stream, thumbnail:str):
        super().__init__(master)
        self.columnconfigure(1, weight = 1)

        self.thumbnail = customtkinter.CTkImage(YouTubeHelper.get_cropped_thumbnail(thumbnail), size=(160,90))
        self.stream = stream

        # image
        self.thumbnail_image = customtkinter.CTkLabel(self, text="", image=self.thumbnail)
        self.thumbnail_image.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky="nswe")
        
        # title
        self.title_label = customtkinter.CTkLabel(self, text=stream.title, font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=1, column=1, columnspan=2, padx=10, pady=(10,5), sticky="nsw")

        # details
        if(stream.type == "video"):
            type = "Video" if stream.is_progressive else "Video Only"
            self.details = f"{type}  ·  {stream.resolution}  ·  {stream.subtype}  ·  {stream.fps}FPS"
        else:
            type = "Audio Only"
            self.details = f"{type}  ·  {stream.subtype}  · {stream.abr}"
        self.video_details_label = customtkinter.CTkLabel(self, text=self.details,
                                                          font=customtkinter.CTkFont(size=12))
        self.video_details_label.grid(row=2, column=1, columnspan=2, padx=10, pady=(0,10), sticky="nsw")

        # progress_bar
        self.progress_bar = customtkinter.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=3, column=1, padx=10, pady=10, sticky="we")

        # percentage
        self.percentage_label = customtkinter.CTkLabel(self, text="0%", font= customtkinter.CTkFont(size=14))
        self.percentage_label.grid(row=3, column=2, padx=10, pady=10, sticky="nsw")

    def progress_update(self, progress:float, percent:int) -> None:
        self.progress_bar.set(progress)
        self.percentage_label.configure(text=f"{percent}%")

        

