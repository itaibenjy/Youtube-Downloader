import customtkinter

class DownloadFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self, text="Downloading")
        self.label.grid(column=0, row=0, sticky="nswe") 
