import customtkinter
from frames.SearchVideoFrame import SearchVideoFrame
from pytube import YouTube
import threading


class SearchPages(customtkinter.CTkTabview):
    def __init__(self, app, master, accent_color:str, fg_color = "transparent"):
        super().__init__(master)
        self.accent_color = accent_color
        self.app = app
        self.lock = threading.Lock()

    def add_video_frame(self, index:int, youtube:YouTube):
        try:
            self.lock.acquire()
            self.add(f"{(index//6) + 1}")
            self.tab(f"{(index//6) + 1}").grid_columnconfigure((0,1,2), weight=1)
            self.lock.release()
        except ValueError:
            self.lock.release()
        new_search_video = SearchVideoFrame(self.app, self.tab(f"{(index//6) + 1}"), youtube, self.accent_color)
        new_search_video.grid(column = (index%6)%3, row = (index%6)//3, padx=5, pady=5, sticky = "nswe")
        new_search_video.setImage()


