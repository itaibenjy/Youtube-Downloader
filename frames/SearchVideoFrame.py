import customtkinter
from pytube import YouTube
from common.YouTubeHelper import YouTubeHelper
from common.HelpTip import HelpTip
from PIL import Image
from threading import Thread

TITLE_LENGTH = 35

class SearchVideoFrame(customtkinter.CTkFrame):
    
    def __init__(self, app, master, youtube:YouTube, accent_color:str):
        self.app = app
        super().__init__(master, border_width=0, border_color=accent_color, width=300, height=200, fg_color=("gray81", "gray20"))
        self.url = youtube.watch_url
        self.thumbnail = youtube.thumbnail_url

        title = youtube.title if len(youtube.title) <= TITLE_LENGTH else youtube.title[:TITLE_LENGTH] + "..."
        self.title_label = customtkinter.CTkLabel(self, text= title, font=customtkinter.CTkFont(size=12))
        self.title_label.grid(row=2, column=1, columnspan=2, pady=5, padx=10, sticky="nsw")
        HelpTip(self.app, self.title_label, message=youtube.title)

        # loading bar
        self.loading_bar = customtkinter.CTkProgressBar(self, mode="indeterminate",width=300)
        self.loading_bar.grid(row=1, column=1, columnspan=2, pady=70, padx=5, sticky="nswe")
        self.loading_bar.start()

        # channel and views
        self.channel_views_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=10))
        try:
            self.channel_views_label.configure(text=f"{youtube.author}  ·  {YouTubeHelper.views_format(youtube.views)} Views")
        except TypeError:
            self.channel_views_label.configure(text=f"{youtube.author}")
        self.channel_views_label.grid(row=3, column=1, pady=(0,5), padx=5, sticky="nsw")
        # liks and date 
        self.duration_date_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=10))
        try:
            self.duration_date_label.configure(text=f"{YouTubeHelper.duration_format(youtube.length)}  ·  {YouTubeHelper.date_format(youtube.publish_date)}")
        except TypeError:
            self.duration_date_label.configure(text=f"{YouTubeHelper.date_format(youtube.publish_date)}")
        self.duration_date_label.grid(row=3, column=2, pady=(0,5), padx=5, sticky="nse")

        # hover effect
        self.bind('<Enter>', lambda *args : self.configure(border_width=4))
        self.bind('<Leave>', lambda *args : self.configure(border_width=0))
        self.title_label.bind('<Enter>', lambda *args : self.configure(border_width=4))
        self.title_label.bind('<Leave>', lambda *args : self.configure(border_width=0))
        self.channel_views_label.bind('<Enter>', lambda *args : self.configure(border_width=4))
        self.channel_views_label.bind('<Leave>', lambda *args : self.configure(border_width=0))
        self.duration_date_label.bind('<Enter>', lambda *args : self.configure(border_width=4))
        self.duration_date_label.bind('<Leave>', lambda *args : self.configure(border_width=0))

        # click on frame
        self.bind("<Button-1>", lambda *args : self.framePressed())
        self.title_label.bind("<Button-1>", lambda *args : self.framePressed())
        self.channel_views_label.bind("<Button-1>", lambda *args : self.framePressed())
        self.duration_date_label.bind("<Button-1>", lambda *args : self.framePressed())
    
    def setImage(self):
        # thumbnail_image
        self.thumbnail_image = customtkinter.CTkImage(YouTubeHelper.get_cropped_thumbnail(self.thumbnail), size=(300, 163))
        self.thumbnail_label_image = customtkinter.CTkLabel(self, text="", image=self.thumbnail_image)

        self.thumbnail_label_image.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="nswe")

        self.thumbnail_label_image.bind('<Enter>', lambda *args : self.configure(border_width=4))
        self.thumbnail_label_image.bind('<Leave>', lambda *args : self.configure(border_width=0))
        self.thumbnail_label_image.bind("<Button-1>", lambda *args : self.framePressed())

        self.loading_bar.destroy()

    def framePressed(self):
        self.app.search_video_event(self.url)
    
