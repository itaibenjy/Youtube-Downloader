import customtkinter
import tkinter
from pytube import YouTube, Stream
from pytube.exceptions import VideoUnavailable, RegexMatchError
from frames.VideoURLFrame import VideoURLFrame
from threading import Thread

class UrlFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.grid_columnconfigure(1,  weight=6)
        self.grid_columnconfigure((0,2,3), weight=1)
        self.rowconfigure(1, weight=1)
 
        self.video_frame = None
        # URL Entry
        self.URL_entry= customtkinter.CTkEntry(self, placeholder_text="Insert a URL")
        self.URL_entry.grid(column=1, row=0, padx=(20,10), pady=20, sticky="nswe") 
        # URL Button 
        self.URL_button = customtkinter.CTkButton(self, text="Find Video", command=self.find_video)
        self.URL_button.grid(column=2, row=0, padx=(10,20), pady=20, sticky="nswe")


    def find_video(self) -> None:
        try:
            self.video_frame = VideoURLFrame(self)
            self.youtube = YouTube(self.URL_entry.get())
            self.video_frame.set_data(self.youtube)
            Thread(target=self.get_streams).start()
        except (VideoUnavailable, RegexMatchError):
            self.video_frame.set_error("YouTube video with the givven URL not found")
        self.video_frame.grid(row=1, column=1, columnspan=2, pady=20, padx=20, sticky="nesw")

    def get_streams(self) -> None:
        self.video_frame.set_type_combobox(self.youtube.streams)


    




