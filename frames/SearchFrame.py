import customtkinter
from frames.SearchPages import SearchPages
from pytube import Search
from common.ColorManager import ColorManager
from threading import Thread

class SearchFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.grid_columnconfigure(1,  weight=6)
        self.grid_columnconfigure((0,2,3), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.app = app 

        # search Entry
        self.search_entry = customtkinter.CTkEntry(self, placeholder_text="Search for a YouTube video")
        self.search_entry.grid(column=1, row=0, padx=(20,10), pady=20, sticky="nswe") 
        # search Button 
        self.search_button = customtkinter.CTkButton(self, text="Search", command = self.search_button_event)
        self.search_button.grid(column=2, row=0, padx=(10,20), pady=20, sticky="nswe")

        self.color_manager = ColorManager()

        self.search_grid = SearchPages(self.app, self, self.color_manager.getColor(self.search_button, "fg_color") )
        self.search_grid.grid(row = 1, column=1, columnspan=2, pady=(0,20), padx = 20, sticky="nswe")
        
        
    def search_button_event(self) -> None:
        search_videos = Search(self.search_entry.get())
        self.search_grid.grid_forget()
        self.search_grid.destroy()
        self.search_grid = SearchPages(self.app, self, self.color_manager.getColor(self.search_button, "fg_color") )
        self.search_grid.grid(row = 1, column=1, columnspan=2, pady=(0,20), padx = 20, sticky="nswe")

        for index in range(len(search_videos.results)):
            Thread(target= lambda *args: self.search_grid.add_video_frame(index, search_videos.results[index])).start()
