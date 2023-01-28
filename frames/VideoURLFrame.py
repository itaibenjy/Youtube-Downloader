import customtkinter
from pytube import YouTube
from PIL import Image
import urllib.request

class VideoURLFrame(customtkinter.CTkFrame):

    def __init__(self, url_frame) -> None:
        super().__init__(url_frame)
        self.video_label = customtkinter.CTkLabel(self, text= "Title", font=customtkinter.CTkFont(size=20))
        self.video_label.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")
        #self.tumbnail_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.thumbnail_image = None
        self.thumbnail_label_image = customtkinter.CTkLabel(self, text="")
        self.thumbnail_label_image.grid(row=2, column=0, columnspan=2, pady=(10,5), padx=20, sticky="nsw")
        
        self.channel_label = customtkinter.CTkLabel(self, text="By channel", font=customtkinter.CTkFont(size=14))
        self.channel_label.grid(row=3, column=0, columnspan=2, pady=(5,10), padx=20, sticky="nsw")
    
    def set_data(self, youtube:YouTube) -> None:
        urllib.request.urlretrieve(youtube.thumbnail_url, "thumbnail.png")
        self.video_label.configure(text=youtube.title)
        self.thumbnail_image =customtkinter.CTkImage(Image.open("thumbnail.png"), size=(600,450))
        self.thumbnail_label_image.configure(image=self.thumbnail_image)
        self.channel_label.configure(text=youtube.author)



