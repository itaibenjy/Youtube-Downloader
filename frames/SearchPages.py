import customtkinter
from frames.SearchVideoFrame import SearchVideoFrame
from pytube import YouTube


class SearchPages(customtkinter.CTkScrollableFrame):
    def __init__(self, app, master, accent_color:str):
        super().__init__(master)
        self.accent_color = accent_color
        self.app = app
        self.grid_columnconfigure(1, weight=1)

    def add_video_frame(self, index:int, youtube:YouTube):
        new_search_video = SearchVideoFrame(self.app, self, youtube, self.accent_color)
        new_search_video.grid(column = index%3, row = index//3, padx=5, pady=5, sticky = "nswe")
        new_search_video.setImage()


