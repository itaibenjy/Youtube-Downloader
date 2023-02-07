import customtkinter
from frames.DownloadVideoFrame import DownloadVideoFrame
from frames.DownloadPages import DownloadPages
from downloads.DownloadManager import DownloadManager
from pytube import Stream
from PIL import Image
from dialogs.InformationDialog import InformationDialog

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
                details = f"Type: {type} \nResulution: {stream.resolution} \nFormat: {stream.subtype} \nFPS: {stream.fps}FPS"
            else:
                type = "Audio Only"
                details = f"Type: {type} \nFormat: {stream.subtype} \nQuality: {stream.abr}"

            if self.dialog is None or not self.dialog.winfo_exists():
                self.dialog = InformationDialog("This video already in downloads", "This video with these details already exist in downloads\n"+ f"{stream.title}\n" + details) 
            else:
                self.dialog.focus()

            return True

        return False


