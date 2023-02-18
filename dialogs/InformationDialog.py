import customtkinter
from common.AssetsController import IconAssets


class InformationDialog(customtkinter.CTkToplevel):
    def __init__(self, title:str, message:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.title(title)
        self.icons = IconAssets()
        self.iconphoto(False, self.icons.info_icon)
        
        self.message_frame = self.get_message(message)
        self.message_frame.grid(row = 1, column = 1, columnspan = 2, padx=20, pady=20, sticky="nswe")

        self.ok_button = customtkinter.CTkButton(self, text="OK", command=self.ok_event)
        self.ok_button.grid(row = 2, column = 2, padx=20, pady=20, sticky="nswe")

        self.attributes('-topmost', 'true')

    def get_message(self, message:str) -> customtkinter.CTkFrame:
        lines = message.split("\n")
        message_frame = customtkinter.CTkFrame(self)
        message_frame.grid_columnconfigure(1, weight=1)
        message_frame.grid_rowconfigure((0,20), weight=1)
        for index,line in enumerate(lines):
            line_label = customtkinter.CTkLabel(message_frame, text=line)
            line_label.grid(row=index+1, column=1,padx = 10, pady=1, sticky="we")
        return message_frame

    def ok_event(self):
        self.destroy()



