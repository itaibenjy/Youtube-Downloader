from os.path import ismount
import tkinter
import customtkinter
from frames.NavigatorFrame import NavigatorFrame
from frames.SearchFrame import SearchFrame
from frames.UrlFrame import UrlFrame
from frames.DownloadFrame import DownloadFrame
from frames.SettingsFrame import SettingsFrame
from common.Enums import Frame
from common.ColorManager import ColorManager
 
ColorManager.setAppearanceMode("Dark")
ColorManager.setTheme("blue")

HEIGHT: int = 1100 
WIDTH: int = 700

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Youtube Downloader")
        self.geometry(f"{HEIGHT}x{WIDTH}")

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

        self.search_frame.frame.grid(row=0, column=1, rowspan= 4, columnspan=3, sticky="nsew")

    # select frame from navigator frame
    def select_frame(self, frame) -> None:
        # removing all frames
        self.search_frame.frame.grid_forget()
        self.url_frame.frame.grid_forget()
        self.download_frame.frame.grid_forget()
        self.settings_frame.frame.grid_forget()
        # showing the chosen screen
        match frame:
            case Frame.SEARCH:
                self.search_frame.frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
            case Frame.URL:
                self.url_frame.frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
            case Frame.DOWNLOADING:
                self.download_frame.frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
            case Frame.SETTINGS:
                self.settings_frame.frame.grid(row=0, column=1, rowspan=4, columnspan=3, sticky="nsew")
                

if __name__ == "__main__":
    app = App()
    app.mainloop()
