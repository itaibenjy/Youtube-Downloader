import customtkinter
from settings.SettingsManager import SettingsManager

class SettingsFrame():

    def __init__(self, app) -> None:
        # setting the frame
        self.frame = customtkinter.CTkFrame(app, fg_color="transparent")
        self.frame.columnconfigure((0,1) , weight= 1)
        self.title = customtkinter.CTkLabel(self.frame, text="Settings", font=customtkinter.CTkFont(size=45, weight="bold"))
        self.title.grid(column=0, row=0, columnspan=2, padx=20, pady=20, sticky="nswe") 

        self.appearance_lable = customtkinter.CTkLabel(self.frame, text="Appearance mode:", font=customtkinter.CTkFont(size=20)) 
        self.appearance_lable.grid(row = 1, column=0, padx=20, pady=(40,10), sticky="nse")
        self.appearance_options = customtkinter.CTkOptionMenu(self.frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_event)
        self.appearance_options.grid(row=1, column=1, padx=20, pady=(40, 10), sticky="nsw")
        self.appearance_options.set(SettingsManager.appearance)
        self.theme_lable = customtkinter.CTkLabel(self.frame, text="Color Theme:", font=customtkinter.CTkFont(size=20)) 
        self.theme_lable.grid(row = 2, column=0, padx=20, pady=(10,10), sticky="nse")
        self.theme_options= customtkinter.CTkOptionMenu(self.frame, values=["Blue", "Green", "Dark Blue"],
                                                                       command=self.change_theme_event)
        self.theme_options.set(SettingsManager.theme.replace("-", " ").title())
        self.theme_options.grid(row=2, column=1, padx=20, pady=(10, 10), sticky="nsw")



    def change_appearance_event(self, appearance:str) -> None:
        SettingsManager.setAppearance(appearance)

    def change_theme_event(self, theme:str) -> None:
        theme_string = theme.replace(" ","-").lower()
        SettingsManager.setTheme(theme_string)


