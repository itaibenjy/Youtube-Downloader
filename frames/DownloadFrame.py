import customtkinter
from frames.DownloadVideoFrame import DownloadVideoFrame
from frames.DownloadPages import DownloadPages
from pytube import Stream
from PIL import Image

class DownloadFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.app = app
        self.title = customtkinter.CTkLabel(self, text="Downloads", font=customtkinter.CTkFont(size=45, weight="bold"))
        self.title.grid(column=1, row=1, padx=20, pady=20, sticky="we") 

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(column=1, row=2, padx=20, pady=20, sticky="nswe")
        self.tabview.add("Completed")
        self.tabview.add("Downloading")


        self.tabview.tab("Downloading").columnconfigure(1, weight=1)
        self.tabview.tab("Downloading").rowconfigure(1, weight=1)
        self.tabview.tab("Completed").columnconfigure(1, weight=1)
        self.tabview.tab("Completed").rowconfigure(1, weight=1)
        
        self.download_frame = DownloadPages(self.tabview.tab("Downloading"))
        self.download_frame.grid(row=1, column=1, sticky="nsew")

        self.completed_frame = DownloadPages(self.tabview.tab("Completed"))
        self.completed_frame.grid(row=1, column=1, sticky="nsew")


    def add_download(self, stream:Stream, thumbnail:Image) -> None:
        self.download_frame.add_element((stream,thumbnail))

    def download_progress(self, stream:Stream, bytes_remaining:int) -> None:
        progress = 1 - (bytes_remaining / stream.filesize)
        percent = int(progress*100)
        self.download_frame.download_progress(stream, progress, percent)
    
    def download_completed(self, stream:Stream, file_path:str):
        thumbnail = self.download_frame.remove_element(stream)
        self.completed_frame.add_element((stream, thumbnail, file_path))

