import customtkinter
import tkinter
from pytube import YouTube, Stream
from pytube.exceptions import VideoUnavailable, RegexMatchError
from frames.VideoFrame import VideoFrame
from threading import Thread

class UrlFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.grid_columnconfigure(1,  weight=6)
        self.grid_columnconfigure((0,2,3), weight=1)
        self.rowconfigure(1, weight=1)

        self.app = app
 
        self.video_frame = None
        # URL Entry
        self.URL_entry= customtkinter.CTkEntry(self, placeholder_text="Insert a URL")
        self.URL_entry.grid(column=1, row=0, padx=(20,10), pady=20, sticky="nswe") 
        # URL Button 
        self.URL_button = customtkinter.CTkButton(self, text="Find Video", command=self.find_video)
        self.URL_button.grid(column=2, row=0, padx=(10,20), pady=20, sticky="nswe")

        self.URL_entry.bind('<Return>',lambda *args: self.find_video())
        
        self.loading_bar = customtkinter.CTkProgressBar(self, mode="indeterminate")

    def find_video(self) -> None:
        self.display_loading_bar()
        Thread(target=self.get_video).start()

    def display_loading_bar(self) -> None:
        if not self.video_frame == None:
            self.video_frame.grid_forget()
        self.URL_entry.configure(state="disabled")
        self.URL_button.configure(state="disabled")
        self.loading_bar.grid(column=1, row=1, columnspan=2, padx=20, pady=40, sticky="we")
        self.loading_bar.start()
    
    def display_video_frame(self) -> None:
        self.URL_entry.configure(state="normal")
        self.URL_button.configure(state="normal")
        self.loading_bar.grid_forget()
        self.loading_bar.stop()
        self.video_frame.grid(row=1, column=1, columnspan=2, pady=20, padx=20, sticky="nesw")

    def get_video(self) -> None:
        try:
            self.video_frame = VideoFrame(self, self.app)
            self.youtube = YouTube(self.URL_entry.get(), on_complete_callback=self.app.download_completed, on_progress_callback=self.app.download_progress)
            self.video_frame.set_data(self.youtube)
            self.video_frame.set_type_combobox(self.youtube.streams)
            self.display_video_frame()
        except (VideoUnavailable, RegexMatchError):
            self.video_frame.set_error("YouTube video with the given URL not found")
            self.display_video_frame()

    def search_video_pressed(self, url:str):
        self.URL_entry.delete(0, len(self.URL_entry.get()))
        self.URL_entry.insert(0,url)
        self.find_video()




    




