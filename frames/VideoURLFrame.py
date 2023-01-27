import customtkinter
from pytube import YouTube
from PIL import Image

class VideoURLFrame():

    def __init__(self, url_frame) -> None:
        self.frame = customtkinter.CTkFrame(url_frame)
        self.video_label = customtkinter.CTkLabel(self.frame, text= "Title", font=customtkinter.CTkFont(size=20))
        self.video_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsw")
        #self.tumbnail_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.thumbnail_image = None
        self.thumbnail_label_image = customtkinter.CTkLabel(self.frame, text="")
        self.thumbnail_label_image.grid(row=1, column=0, columnspan=2, pady=(10,5), sticky="nsw")
        
        self.channel_label = customtkinter.CTkLabel(self.frame, text="By channel", font=customtkinter.CTkFont(size=14))
        self.channel_label.grid(row=1, column=0, columnspan=2, pady=(5,10), sticky="nsw")
    
    def set_data(self, youtube:YouTube) -> None:
        self.video_label.configure(text=youtube.title)
        self.thumbnail_image =customtkinter.CTkImage(Image.open(), size=(240,135))
        self.thumbnail_label_image.configure(image=self.thumbnail_image)
        self.channel_label.configure(text=youtube.channel_id)


