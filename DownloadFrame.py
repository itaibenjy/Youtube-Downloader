import customtkinter

class DownloadFrame():

    def __init__(self, app) -> None:
        # setting the frame
        self.frame = customtkinter.CTkFrame(app, fg_color="transparent")
        self.label = customtkinter.CTkLabel(self.frame, text="Downloading")
        self.label.grid(column=0, row=0, sticky="nswe") 
