import customtkinter
from pytube import YouTube
from PIL import Image
from urllib.request import urlopen

class VideoURLFrame(customtkinter.CTkFrame):

    def __init__(self, url_frame) -> None:
        super().__init__(url_frame)
        self.title_label = customtkinter.CTkLabel(self, text= "", font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")
        #self.tumbnail_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.thumbnail_image = None
        self.thumbnail_label_image = customtkinter.CTkLabel(self, text="")
        self.thumbnail_label_image.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")
        
        self.channel_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=14))
        self.channel_label.grid(row=3, column=0, columnspan=2, pady=(0,10), padx=20, sticky="nsw")

    def set_data(self, youtube:YouTube) -> None:
        self.title_label.configure(text=youtube.title)
        self.thumbnail_image =customtkinter.CTkImage(Image.open(urlopen(youtube.thumbnail_url)), size=(600,450))
        self.thumbnail_label_image.configure(image=self.thumbnail_image)
        self.channel_label.configure(text=youtube.author)

    def set_error(self, error:str) -> None:
        self.thumbnail_label_image.configure(image='')
        self.channel_label.configure(text="")
        self.title_label.configure(text=error)



