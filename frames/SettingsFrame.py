import customtkinter
from settings.SettingsManager import SettingsManager
from tkinter import filedialog

class SettingsFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.columnconfigure((0,1) , weight= 1)
        self.settings_frame = customtkinter.CTkFrame(self)
        self.title = customtkinter.CTkLabel(self, text="Settings", font=customtkinter.CTkFont(size=45, weight="bold"))
        self.title.grid(column=0, row=0, columnspan=2, padx=20, pady=20, sticky="nswe") 

        self.appearance_lable = customtkinter.CTkLabel(self.settings_frame, text="Appearance mode:", font=customtkinter.CTkFont(size=20)) 
        self.appearance_lable.grid(row = 1, column=0, padx=20, pady=(40,10), sticky="e")
        self.appearance_options = customtkinter.CTkOptionMenu(self.settings_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_event)
        self.appearance_options.grid(row=1, column=1, padx=20, pady=(40, 10), sticky="nsw")
        self.appearance_options.set(SettingsManager.appearance)
        self.theme_lable = customtkinter.CTkLabel(self.settings_frame, text="Color Theme:", font=customtkinter.CTkFont(size=20)) 
        self.theme_lable.grid(row = 2, column=0, padx=20, pady=(10,10), sticky="nse")
        self.theme_options= customtkinter.CTkOptionMenu(self.settings_frame, values=["Blue", "Green", "Dark Blue"],
                                                                       command=self.change_theme_event)
        self.theme_options.set(SettingsManager.theme.replace("-", " ").title())
        self.theme_options.grid(row=2, column=1, padx=20, pady=(10, 10), sticky="nsw")

        self.download_label = customtkinter.CTkLabel(self.settings_frame, text="Download Location:", font=customtkinter.CTkFont(size=20)) 
        self.download_label.grid(row = 3, column=0, padx=20, pady=(10,5), sticky="nse")

        self.location_lable = customtkinter.CTkLabel(self.settings_frame, text=SettingsManager.download_folder, font=customtkinter.CTkFont(size=12)) 
        self.location_lable.grid(row = 3, column=1, padx=20, pady=(10,5), sticky="nsw")

        self.browse_button = customtkinter.CTkButton(self.settings_frame, text="Browse",command=self.browse_event)
        self.browse_button.grid(row=4, column=1, padx=20, pady=(5,10), sticky="nsw")

        self.settings_frame.grid(row=1, column=0, columnspan=2, sticky="s")



    def change_appearance_event(self, appearance:str) -> None:
        SettingsManager.setAppearance(appearance)

    def change_theme_event(self, theme:str) -> None:
        theme_string = theme.replace(" ","-").lower()
        SettingsManager.setTheme(theme_string)

    def browse_event(self) -> None:
        folder_path = filedialog.askdirectory()
        self.location_lable.configure(text=folder_path)
        SettingsManager.setFolder(folder_path)



