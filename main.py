from os.path import ismount
import os
import tkinter
import customtkinter
from frames.NavigatorFrame import NavigatorFrame
from frames.SearchFrame import SearchFrame
from frames.UrlFrame import UrlFrame
from frames.DownloadFrame import DownloadFrame
from frames.SettingsFrame import SettingsFrame
from common.Enums import Frame
from common.AssetsController import IconAssets
from settings.SettingsManager import SettingsManager
from downloads.DownloadManager import DownloadManager
from pytube import Stream
from PIL import Image
 
SettingsManager.setSettings()

HEIGHT: int = 700 
WIDTH: int = 1100

def restart_app(app) -> None:
    app.destroy()
    app = App()
    app.setDownloads()
    app.mainloop()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Youtube Downloader")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.icons = IconAssets()
        self.iconphoto(False, self.icons.main_icon)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # frames
        self.navigator_frame = NavigatorFrame(self)
        self.search_frame = SearchFrame(self)
        self.url_frame = UrlFrame(self)
        self.download_frame = DownloadFrame(self)
        self.settings_frame = SettingsFrame(self)
        
        # setting the search frame to be default frame
        self.search_frame.grid(row=0, column=1, rowspan= 4, columnspan=3, sticky="nsew")

    # select frame from navigator frame
    def select_frame(self, frame) -> None:
        # removing all frames
        self.search_frame.grid_forget()
        self.url_frame.grid_forget()
        self.download_frame.grid_forget()
        self.settings_frame.grid_forget()
        # showing the chosen screen
        match frame:
            case Frame.SEARCH:
                self.search_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
            case Frame.URL:
                self.url_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
            case Frame.DOWNLOADING:
                self.download_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
            case Frame.SETTINGS:
                self.settings_frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")

    def restart_app(self) -> None:
        restart_app(self)

    def add_to_downloads(self, stream:Stream, thumbnail:str) -> None:
        self.download_frame.add_download(stream, thumbnail)
        self.navigator_frame.downloading_button_event()
        self.download_frame.tabview.set("Downloading")

    def download_progress(self, stream:Stream, chunk, bytes_remaining) -> None:
        self.download_frame.download_progress(stream, bytes_remaining)

    def download_completed(self, stream:Stream, file_path:str) -> None:
        self.download_frame.download_completed(stream, file_path)
    
    def setDownloads(self) -> None:
        DownloadManager.setDownloads(self.download_frame)

    def search_video_event(self, url:str):
        self.navigator_frame.url_button_event()
        self.url_frame.search_video_pressed(url)

    def download_already_exist(self, stream:Stream, thumbnail:str) -> bool:
        return self.download_frame.is_already_exist(stream, thumbnail)

if __name__ == "__main__":
    app = App()
    app.setDownloads()
    app.mainloop()
