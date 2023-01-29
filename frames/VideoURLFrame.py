import customtkinter
from pytube import YouTube
from PIL import Image
from frames.ScrollableFrame import ScrollableFrame
from common.YouTubeHelper import YouTubeHelper
from urllib.request import urlopen

class VideoURLFrame(ScrollableFrame):

    def __init__(self, url_frame) -> None:
        super().__init__(url_frame)
        self.title_label = customtkinter.CTkLabel(self.scrollable_frame, text= "", font=customtkinter.CTkFont(size=18))
        self.title_label.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")

        # thumbnail_image
        self.thumbnail_image = None
        self.thumbnail_label_image = customtkinter.CTkLabel(self.scrollable_frame, text="")
        self.thumbnail_label_image.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")
        
        # channel and views
        self.channel_views_label = customtkinter.CTkLabel(self.scrollable_frame, text="", font=customtkinter.CTkFont(size=12))
        self.channel_views_label.grid(row=3, column=0, columnspan=2, pady=(0,10), padx=20, sticky="nsw")
    
    # set youtube data
    def set_data(self, youtube:YouTube) -> None:
        self.title_label.configure(text=youtube.title)
        self.thumbnail_image =customtkinter.CTkImage(Image.open(urlopen(youtube.thumbnail_url)), size=(600,450))
        self.thumbnail_label_image.configure(image=self.thumbnail_image)
        self.channel_views_label.configure(text=f"{youtube.author} · {YouTubeHelper.views_format(youtube.views)} Views")
        self.youtube = youtube
    
    # set error
    def set_error(self, error:str) -> None:
        self.title_label.configure(text=error)
    


