import customtkinter
import sys
from frames.DownloadVideoFrame import DownloadVideoFrame
from frames.DownloadPages import DownloadPages
from downloads.DownloadManager import DownloadManager
from common.CombineManager import CombineManager
from pytube import Stream
from PIL import Image
from dialogs.InformationDialog import InformationDialog
from threading import Thread
import proglog

class DownloadFrame(customtkinter.CTkFrame):

    def __init__(self, app) -> None:
        # setting the frame
        super().__init__(app, fg_color="transparent")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.app = app
        self.title = customtkinter.CTkLabel(self, text="Downloads", font=customtkinter.CTkFont(size=45, weight="bold"))
        self.title.grid(column=1, row=1, padx=20, pady=20, sticky="we") 

        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(column=1, row=2, padx=20, pady=20, sticky="nswe")
        self.tabview.add("Completed")
        self.tabview.add("Downloading")


        self.tabview.tab("Downloading").columnconfigure(1, weight=1)
        self.tabview.tab("Downloading").rowconfigure(1, weight=1)
        self.tabview.tab("Completed").columnconfigure(1, weight=1)
        self.tabview.tab("Completed").rowconfigure(1, weight=1)
        
        self.download_frame = DownloadPages(self.tabview.tab("Downloading"))
        self.download_frame.grid(row=1, column=1, sticky="nsew")

        self.completed_frame = DownloadPages(self.tabview.tab("Completed"))
        self.completed_frame.grid(row=1, column=1, sticky="nsew")

        self.combine_frame = customtkinter.CTkFrame(self.tabview.tab("Completed"))
        self.combine_frame.grid_columnconfigure((1,0) , weight=1)
        self.combine_frame.grid(row=2, column=1, pady=5, sticky="nsew")

        self.combine_text = customtkinter.CTkLabel(self.combine_frame, text="Combine Mode: ", font=customtkinter.CTkFont(size=22) )
        self.combine_text.grid(row=0, column=0, pady=10, padx=10, sticky="nse")

        self.switch_var = customtkinter.StringVar(value="on")
        self.combine_switch = customtkinter.CTkSwitch(self.combine_frame, text="", command=self.switch_event, variable=self.switch_var, onvalue="on", offvalue="off")
        self.combine_switch.deselect()
        self.combine_switch.grid(row=0, column=1, pady=10, padx=10, sticky="nsw")

        self.combine_button = customtkinter.CTkButton(self.combine_frame, text="Combine", command=self.combine_event)

        self.progress_frame = customtkinter.CTkFrame(self.tabview.tab("Completed"))
        self.progress_frame.grid_columnconfigure(1 , weight=1)

        self.progress_bar = customtkinter.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.progress_label = customtkinter.CTkLabel(self.progress_frame, text="")
        self.progress_label.grid(row=0, column=0, pady=10, padx=10, sticky="nswe")
        self.progress_percentage = customtkinter.CTkLabel(self.progress_frame, text="")
        self.progress_percentage.grid(row=0, column=2, pady=10, padx=10, sticky="nswe")

        self.dialog = None


    def add_download(self, stream:Stream, thumbnail:str) -> None:
        self.download_frame.add_element((stream,thumbnail))

    def download_progress(self, stream:Stream, bytes_remaining:int) -> None:
        progress = 1 - (bytes_remaining / stream.filesize)
        percent = int(progress*100)
        self.download_frame.download_progress(stream, progress, percent)
    
    def download_completed(self, stream:Stream, file_path:str):
        thumbnail = self.download_frame.remove_element(stream)
        data = self.downloadToDict(stream, file_path, thumbnail)
        DownloadManager.saveToCompleted(data)
        self.completed_frame.add_element([data])
        self.tabview.set("Completed")

    def add_to_completed_downloads(self, stream_data:dict) ->  None:
        self.completed_frame.add_element([stream_data])
    
    def downloadToDict(self, stream: Stream, file_path:str, thumbnail:str) -> dict:
        dictionary:dict = {}
        dictionary["file_path"] = file_path
        dictionary["thumbnail"] = thumbnail
        dictionary["file_size"] = stream.filesize_mb
        dictionary["title"] = stream.title
        if(stream.type == "video"):
            streamType = "Video" if stream.is_progressive else "Video Only"
            dictionary["details"] = f"{streamType}  ·  {stream.resolution}  ·  {stream.subtype}  ·  {stream.fps}FPS"
        else:
            streamType = "Audio Only"
            dictionary["details"] = f"{streamType}  ·  {stream.subtype}  · {stream.abr}"
        return dictionary

    def is_already_exist(self, stream:Stream, thumbnail:str) -> bool:
        if DownloadManager.is_already_exist(self.downloadToDict(stream, "","")) or (stream,thumbnail) in self.download_frame.elements:
            
            if(stream.type == "video"):
                type = "Video" if stream.is_progressive else "Video Only"
                details = f"Type: {type} \nResolution: {stream.resolution} \nFormat: {stream.subtype} \nFPS: {stream.fps}FPS"
            else:
                type = "Audio Only"
                details = f"Type: {type} \nFormat: {stream.subtype} \nQuality: {stream.abr}"

            if self.dialog is not None and self.dialog.winfo_exists():
                self.dialog.destroy()
            self.dialog = InformationDialog("This video already in downloads", "This video with these details already exist in downloads\n"+ f"{stream.title}\n" + details) 

            return True

        return False

    def switch_event(self) -> None:
        CombineManager.is_combine_mode = not CombineManager.is_combine_mode
        self.completed_frame.rerender_elements()
        if CombineManager.is_combine_mode:
            self.combine_button.grid(row=0, column=1, pady=10, padx=(0, 20), sticky="nse")
        else:
            self.combine_button.grid_forget()

    def combine_event(self) -> None:
        if CombineManager.amount_selected != 2:
            if self.dialog is not None and self.dialog.winfo_exists():
                self.dialog.destroy()

            self.dialog = InformationDialog("Can't Combine selected downloads!", "The selected Downloads are not compatible for combining \nTo be able to combine two downloads choose\n"+ "one Download of type Only Audio and other of type \nOnly Video of the same youtube video than press combine") 
        else:
            self.switch_event()
            Thread(target = self.combine_in_thread).start()
    
    def combine_in_thread(self) -> None:
        self.combine_frame.grid_forget()
        self.progress_frame.grid(row=2, column=1, pady=5, sticky="nsew")
        CombineManager.combine_chosen_downloads(self.completed_frame, self.progress_label, self.progress_bar, self.progress_percentage)
        self.progress_frame.grid_forget()
        self.combine_frame.grid(row=2, column=1, pady=5, sticky="nsew")
