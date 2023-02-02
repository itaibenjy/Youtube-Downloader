import customtkinter
from pytube import YouTube, Stream
from PIL import Image
from pytube.exceptions import PytubeError
from frames.ScrollableFrame import ScrollableFrame
from common.YouTubeHelper import YouTubeHelper
from settings.SettingsManager import SettingsManager
from urllib.request import urlopen
import bordercrop
from threading import Thread
import copy 

class VideoFrame(customtkinter.CTkTabview):

    def __init__(self, master_frame, app) -> None:
        super().__init__(master_frame, state="disabled")
        
        self.add("Video Details")
        self.add("Download")
        self.tab("Video Details").columnconfigure((0,3), weight=1)
        self.tab("Download").columnconfigure((0,3), weight=1)
        self.tab("Download").rowconfigure(0, weight=1)
        self.tab("Download").rowconfigure(10, weight=2)

        self.app = app

        self.title_label = customtkinter.CTkLabel(self.tab("Video Details"), text= "", font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=2, column=1, columnspan=2, pady=10, padx=20, sticky="nsw")

        self.download_label = customtkinter.CTkLabel(self.tab("Download"), text= "Download Details", font=customtkinter.CTkFont(size=45, weight="bold"))
        self.download_label.grid(row=1, column=0, columnspan=4, pady=20, padx=20, sticky="ns")

        # thumbnail_image
        self.thumbnail_image = None
        self.thumbnail_label_image = customtkinter.CTkLabel(self.tab("Video Details"), text="")
        self.thumbnail_label_image.grid(row=1, column=1, columnspan=2, pady=10, padx=20, sticky="nsw")
        
        # channel and views
        self.channel_views_label = customtkinter.CTkLabel(self.tab("Video Details"), text="", font=customtkinter.CTkFont(size=14))
        self.channel_views_label.grid(row=3, column=1, pady=(0,10), padx=20, sticky="nsw")
        # liks and date 
        self.duration_date_label = customtkinter.CTkLabel(self.tab("Video Details"), text="", font=customtkinter.CTkFont(size=14))
        self.duration_date_label.grid(row=3, column=2, pady=(0,10), padx=20, sticky="nse")
    
        # comboboxes to choose a streams
        # labels
        self.type_label = customtkinter.CTkLabel(self.tab("Download"), text="Type: ", font=customtkinter.CTkFont(size=20))
        self.type_label.grid(row=2, column=1, pady=10, padx=20, sticky="nsw")
        self.resolution_label = customtkinter.CTkLabel(self.tab("Download"), text="Resolution: ", font=customtkinter.CTkFont(size=20))
        self.resolution_label.grid(row=3, column=1, pady=10, padx=20, sticky="nsw")
        self.format_label = customtkinter.CTkLabel(self.tab("Download"), text="Format: ", font=customtkinter.CTkFont(size=20))
        self.format_label.grid(row=4, column=1, pady=10, padx=20, sticky="nsw")
        self.fps_label = customtkinter.CTkLabel(self.tab("Download"), text="FPS: ", font=customtkinter.CTkFont(size=20))

        # comboboxes
        self.type_combobox = customtkinter.CTkOptionMenu(self.tab("Download"), values=[], command=self.type_combobox_event, state='disabled')
        self.type_combobox.set("Wait a second")
        self.type_combobox.grid(row=2, column=2, pady=10, padx=20, sticky="nse")
        self.resolution_combobox = customtkinter.CTkOptionMenu(self.tab("Download"), values=[], command=self.resolution_combobox_event, state='disabled')
        self.resolution_combobox.set("Wait a second")
        self.resolution_combobox.grid(row=3, column=2, pady=10, padx=20, sticky="nse")
        self.format_combobox = customtkinter.CTkOptionMenu(self.tab("Download"), values=[], command=self.format_combobox_event, state='disabled')
        self.format_combobox.set("Wait a second")
        self.format_combobox.grid(row=4, column=2, pady=10, padx=20, sticky="nse")
        self.fps_combobox = customtkinter.CTkOptionMenu(self.tab("Download"), values=[], command=self.fps_combobox_event, state='disabled')

        # Download Button
        self.download_button = customtkinter.CTkButton(self.tab("Download"), text="Download", command=self.download_button_event, state='disabled') 
        self.download_button.grid(row=6, column=1, columnspan=2, pady=20, padx=20, sticky="ns")

    # set youtube data
    def set_data(self, youtube:YouTube) -> None:
        try:
            self.title_label.configure(text=youtube.title)
        except PytubeError:
            self.set_error("Error while retriving the video, try again.")
            return
        try:
            self.thumbnail_image =customtkinter.CTkImage(bordercrop.crop(youtube.thumbnail_url, MINIMUM_ROWS=10), size=(800,450))
        except ValueError:
           self.thumbnail_image = customtkinter.CTkImage(Image.open(urlopen(youtube.thumbnail_url)), size=(600, 450))
        self.thumbnail_label_image.configure(image=self.thumbnail_image)
        self.channel_views_label.configure(text=f"{youtube.author}  ·  {YouTubeHelper.views_format(youtube.views)} Views")
        self.duration_date_label.configure(text=f"{YouTubeHelper.duration_format(youtube.length)}  ·  {YouTubeHelper.date_format(youtube.publish_date)}")
        self.youtube = youtube
        self.configure(state="normal")
        
    
    # set error
    def set_error(self, error:str) -> None:
        self.title_label.configure(text=error)
        self.configure(state="disabled")

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
            self.type_streams = YouTubeHelper.filter_streams(self.streams, type=self.type_value.replace(" Only", "").lower())

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
        if self.type_value == "Video" or self.type_value == "Video Only":
            self.fps_combobox.configure(values=YouTubeHelper.get_filter_values(self.format_streams,"fps"), state="normal")
            self.fps_value:str = self.fps_combobox.cget("values")[0]
            self.fps_combobox.set(self.fps_value)
            self.fps_combobox.grid(row=5, column=2, pady=10, padx=20, sticky="nse")
            self.fps_label.grid(row=5, column=1, pady=10, padx=20, sticky="nsw")
        else:
            self.fps_combobox.grid_forget()
            self.fps_label.grid_forget()

        self.fps_combobox_event(self.fps_value)

    def fps_combobox_event(self, selected:str) -> None:
        self.fps_value = selected
        self.selected_streams = YouTubeHelper.filter_streams(self.format_streams, fps=int(self.fps_value))
        self.download_button.configure(state="normal")

    def download_button_event(self) -> None:
        # possibly put in thread
        stream = self.selected_streams[0]
        try:
            thumbnail_image = customtkinter.CTkImage(bordercrop.crop(self.youtube.thumbnail_url, MINIMUM_ROWS=10), size=(160,90))
        except ValueError:
            thumbnail_image = customtkinter.CTkImage(Image.open(urlopen(self.youtube.thumbnail_url)), size=(120, 90))
        self.app.add_to_downloads(stream, thumbnail_image)
        Thread(target=lambda : self.download_stream(stream)).start()
    
    def download_stream(self, stream:Stream) -> None:
        if stream.type == "video":
            stream.download(output_path=SettingsManager.download_folder,
                            filename=f"{stream.title.replace(' ','')}_{stream.resolution}_{stream.fps}fps.{stream.subtype}")
        else:
            stream.download(output_path=SettingsManager.download_folder,
                            filename=f"{stream.title.replace(' ','')}_{stream.abr}.{stream.subtype}")





