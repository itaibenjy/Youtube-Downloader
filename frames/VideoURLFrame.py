import customtkinter
from pytube import YouTube, Stream
from PIL import Image
from frames.ScrollableFrame import ScrollableFrame
from common.YouTubeHelper import YouTubeHelper
from urllib.request import urlopen

class VideoURLFrame(ScrollableFrame):

    def __init__(self, url_frame) -> None:
        super().__init__(url_frame)
        self.title_label = customtkinter.CTkLabel(self.scrollable_frame, text= "", font=customtkinter.CTkFont(size=18))
        self.title_label.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")

        # thumbnail_image
        self.thumbnail_image = None
        self.thumbnail_label_image = customtkinter.CTkLabel(self.scrollable_frame, text="")
        self.thumbnail_label_image.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="nsw")
        
        # channel and views
        self.channel_views_label = customtkinter.CTkLabel(self.scrollable_frame, text="", font=customtkinter.CTkFont(size=12))
        self.channel_views_label.grid(row=3, column=0, columnspan=2, pady=(0,10), padx=20, sticky="nsw")
    
        # comboboxes to choose a streams
        # labels
        self.type_label = customtkinter.CTkLabel(self.scrollable_frame, text="Type: ", font=customtkinter.CTkFont(size=14))
        self.type_label.grid(row=4, column=0, pady=10, padx=20, sticky="nsw")
        self.resolution_label = customtkinter.CTkLabel(self.scrollable_frame, text="Resolution: ", font=customtkinter.CTkFont(size=14))
        self.resolution_label.grid(row=5, column=0, pady=10, padx=20, sticky="nsw")
        self.format_label = customtkinter.CTkLabel(self.scrollable_frame, text="Format: ", font=customtkinter.CTkFont(size=14))
        self.format_label.grid(row=6, column=0, pady=10, padx=20, sticky="nsw")
        self.fps_label = customtkinter.CTkLabel(self.scrollable_frame, text="FPS: ", font=customtkinter.CTkFont(size=14))

        # comboboxes
        self.type_combobox = customtkinter.CTkOptionMenu(self.scrollable_frame, values=[], command=self.type_combobox_event, state='disabled')
        self.type_combobox.set("Wait a second")
        self.type_combobox.grid(row=4, column=1, pady=10, padx=20, sticky="nsw")
        self.resolution_combobox = customtkinter.CTkOptionMenu(self.scrollable_frame, values=[], command=self.resolution_combobox_event, state='disabled')
        self.resolution_combobox.set("Wait a second")
        self.resolution_combobox.grid(row=5, column=1, pady=10, padx=20, sticky="nsw")
        self.format_combobox = customtkinter.CTkOptionMenu(self.scrollable_frame, values=[], command=self.format_combobox_event, state='disabled')
        self.format_combobox.set("Wait a second")
        self.format_combobox.grid(row=6, column=1, pady=10, padx=20, sticky="nsw")
        self.fps_combobox = customtkinter.CTkOptionMenu(self.scrollable_frame, values=[], command=self.fps_combobox_event, state='disabled')


    # set youtube data
    def set_data(self, youtube:YouTube) -> None:
        self.title_label.configure(text=youtube.title)
        self.thumbnail_image =customtkinter.CTkImage(Image.open(urlopen(youtube.thumbnail_url)), size=(600,450))
        self.thumbnail_label_image.configure(image=self.thumbnail_image)
        self.channel_views_label.configure(text=f"{youtube.author} · {YouTubeHelper.views_format(youtube.views)} Views")
        self.youtube = youtube
    
    # set error
    def set_error(self, error:str) -> None:
        self.title_label.configure(text=error)

    def set_type_combobox(self, streams:list[Stream]):
        self.type_combobox.configure(values=YouTubeHelper.get_filter_values(streams,"type"), state="normal")
        self.type_value:str = self.type_combobox.cget("values")[0]
        self.type_combobox.set(self.type_value)
        self.streams = streams
        self.type_combobox_event(self.type_value)
    

    def type_combobox_event(self, selected:str):
        self.type_value = selected
        if self.type_value == "Video":
            self.type_streams = YouTubeHelper.filter_streams(self.streams, progressive=True)
        else:
            self.type_streams = YouTubeHelper.filter_streams(self.streams, type=self.type_value.replace("Only ", ""))

        self.resolution_combobox.configure(values=YouTubeHelper.get_filter_values(self.type_streams,"res"), state="normal")
        self.resolution_value:str = self.resolution_combobox.cget("values")[0]
        self.resolution_combobox.set(self.resolution_value)
        self.resolution_combobox_event(self.resolution_value)

    
    def resolution_combobox_event(self, selected:str):
        self.resolution_value =  selected
        self.resolution_streams = YouTubeHelper.filter_streams(self.type_streams, res=self.resolution_value)
        self.format_combobox.configure(values=YouTubeHelper.get_filter_values(self.resolution_streams,"format"), state="normal")
        self.format_value:str = self.format_combobox.cget("values")[0]
        self.format_combobox.set(self.format_value)
        self.format_combobox_event(self.format_value)

    def format_combobox_event(self, selected:str):
        self.format_value = selected
        self.format_streams = YouTubeHelper.filter_streams(self.resolution_streams, format=self.format_value)
        if self.type_value == "Video" or self.type_value == "Only video":
            self.fps_combobox.configure(values=YouTubeHelper.get_filter_values(self.format_streams,"fps"), state="normal")
            self.fps_value:str = self.fps_combobox.cget("values")[0]
            self.fps_combobox.set(self.fps_value)
            self.fps_combobox.grid(row=7, column=1, pady=10, padx=20, sticky="nsw")
            self.fps_label.grid(row=7, column=0, pady=10, padx=20, sticky="nsw")
        else:
            self.fps_combobox.grid_forget()
            self.fps_label.grid_forget()

        self.fps_combobox_event(self.fps_value)

    def fps_combobox_event(self, selected:str):
        self.fps_value = selected
        self.selected_streams = YouTubeHelper.filter_streams(self.format_streams, fps=int(self.fps_value))
        print(self.selected_streams)
