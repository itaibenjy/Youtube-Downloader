import customtkinter
from common.AssetsController import NavigatorAssets
from common.Enums import Frame
from common.HelpTip import HelpTip



class NavigatorFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # saving the app 
        self.app = app
        

        # getting access to all necessary assets
        self.assets = NavigatorAssets()

        # setting the frame
        super().__init__(app, width=2, corner_radius=0)
        self.grid(row=0, column=0, rowspan= 4, sticky="nsew")

        button = customtkinter.CTkButton(self,text="")
        self.SELECT_COLOR:tuple = button.cget("fg_color")
        self.SELECT_COLOR_HOVER:tuple = button.cget("hover_color")
        self.HOVER_COLOR:tuple = ("gray70", "gray30");
        self.TEXT_COLOR:tuple = ("gray10", "gray90");

        self.BUTTON_HEIGHT:int = 55;

        # configure 6X1
        self.grid_rowconfigure(1,  weight=1)
        self.grid_rowconfigure(5,  weight=3)

        # Title - Youtube Downloader
        self.title = customtkinter.CTkLabel(self, text="", image=self.assets.logo_icon)
        self.title.grid(row=0, column=0, padx=10, pady=40)

        # Navigation Buttons 
        self.search = customtkinter.CTkButton(self, corner_radius=0, height=self.BUTTON_HEIGHT, border_spacing=10, text="",
                                              width= 60, fg_color=self.SELECT_COLOR, text_color=self.TEXT_COLOR, hover_color=self.HOVER_COLOR,
                                              image=self.assets.search_icon,command=self.search_button_event)
        self.search.grid(row=2, column=0, sticky="ew")
        HelpTip(self.app, self.search, message="Search for a YouTube video")

        self.url = customtkinter.CTkButton(self, corner_radius=0, height=self.BUTTON_HEIGHT, border_spacing=10, text="",
                                              width= 60, fg_color="transparent", text_color=self.TEXT_COLOR, hover_color=self.HOVER_COLOR,
                                              image=self.assets.url_icon,command=self.url_button_event)
        self.url.grid(row=3, column=0, sticky="ew")
        HelpTip(self.app, self.url, message="Find by URL")

        self.downloading = customtkinter.CTkButton(self, corner_radius=0, height=self.BUTTON_HEIGHT, border_spacing=10, text="",
                                              width= 60, fg_color="transparent", text_color=self.TEXT_COLOR, hover_color=self.HOVER_COLOR,
                                              image=self.assets.download_icon,command=self.downloading_button_event)
        self.downloading.grid(row=4, column=0, sticky="ew")
        HelpTip(self.app, self.downloading, message="View Downloads")

        self.settings = customtkinter.CTkButton(self, corner_radius=0, height=self.BUTTON_HEIGHT, border_spacing=10, text="",
                                              width= 60, fg_color="transparent", text_color=self.TEXT_COLOR, hover_color=self.HOVER_COLOR,
                                              image=self.assets.settings_icon,command=self.settings_button_event)
        self.settings.grid(row=6, column=0, sticky="sew")
        HelpTip(self.app, self.settings, message="View Settings")

 
    # Methods

    # select the button that was pressed and invoke app method to change frame
    def select_frame(self, frame: Frame) -> None:
        # make all the buttons transparent
        self.search.configure(fg_color="transparent", hover_color=self.HOVER_COLOR)
        self.url.configure(fg_color="transparent", hover_color=self.HOVER_COLOR)
        self.downloading.configure(fg_color="transparent", hover_color=self.HOVER_COLOR)
        self.settings.configure(fg_color="transparent", hover_color=self.HOVER_COLOR)

        # update which button was selected
        match frame:
            case Frame.SEARCH:
                self.search.configure(fg_color=self.SELECT_COLOR, hover_color=self.SELECT_COLOR_HOVER)
            case Frame.URL:
                self.url.configure(fg_color=self.SELECT_COLOR, hover_color=self.SELECT_COLOR_HOVER)
            case Frame.DOWNLOADING:
                self.downloading.configure(fg_color=self.SELECT_COLOR, hover_color=self.SELECT_COLOR_HOVER)
            case Frame.SETTINGS:
                self.settings.configure(fg_color=self.SELECT_COLOR, hover_color=self.SELECT_COLOR_HOVER)
        # invoke the app method to display the frame that was selected
        self.app.select_frame(frame)

    # method that gets invoked when pressing the buttons in the navigation bar.
    def search_button_event(self) -> None:
        self.select_frame(Frame.SEARCH)
    
    def url_button_event(self) -> None:
        self.select_frame(Frame.URL)

    def downloading_button_event(self) -> None:
        self.select_frame(Frame.DOWNLOADING)

    def settings_button_event(self) -> None:
        self.select_frame(Frame.SETTINGS)
