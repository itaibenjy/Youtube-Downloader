import customtkinter


class SearchFrame():

    def __init__(self, app) -> None:
        # setting the frame
        self.frame = customtkinter.CTkFrame(app, fg_color="transparent")
        self.frame.grid_columnconfigure(1,  weight=6)
        self.frame.grid_columnconfigure((0,2,3), weight=1)

        # search Entry
        self.search_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Search for a YouTube video")
        self.search_entry.grid(column=1, row=0, padx=(20,10), pady=20, sticky="nswe") 
        # search Button 
        self.search_button = customtkinter.CTkButton(self.frame, text="Search")
        self.search_button.grid(column=2, row=0, padx=(10,20), pady=20, sticky="nswe")
