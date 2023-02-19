import customtkinter
from pytube import Stream
from PIL import Image
import os
import subprocess
from common.HelpTip import HelpTip
from common.AssetsController import DownloadAssets
from downloads.DownloadManager import DownloadManager
from common.YouTubeHelper import YouTubeHelper
from common.CombineManager import CombineManager
from dialogs.AlertDialog import AlertDialog

TITLE_LENGTH = 60
HOVER_COLOR = ("gray70", "gray30");

class CompletedVideoFrame(customtkinter.CTkFrame):
    def __init__(self, downloadPages, stream_data: dict):
        super().__init__(downloadPages)

        self.downloadPages = downloadPages

        self.stream_data = stream_data

        self.grid_columnconfigure(2, weight = 1)

        self.thumbnail = customtkinter.CTkImage(YouTubeHelper.get_cropped_thumbnail(stream_data["thumbnail"]), size=(160,90))

        self.file_path = stream_data["file_path"]

        self.assets =  DownloadAssets()

        # image
        self.thumbnail_image = customtkinter.CTkLabel(self, text="", image=self.thumbnail)
        self.thumbnail_image.grid(row=1, column=1, rowspan=3, padx=10, pady=10, sticky="nsw")
        
        # title
        title = stream_data["title"] if len(stream_data["title"]) <= TITLE_LENGTH else stream_data["title"][:TITLE_LENGTH] + "..."
        self.title_label = customtkinter.CTkLabel(self, text=title, font=customtkinter.CTkFont(size=20))
        self.title_label.grid(row=1, column=2, columnspan=2, padx=10, pady=(10,5), sticky="nsw")
        HelpTip(downloadPages, self.title_label, message=stream_data["title"])

        # details
        # checking if the stream file exists in the download path 
        if not os.path.isfile(stream_data["file_path"]):
            self.video_details_label = customtkinter.CTkLabel(self, text="FILE NOT FOUND!",
                                                            font=customtkinter.CTkFont(size=12))
        else: 
            self.video_details_label = customtkinter.CTkLabel(self, text=stream_data["details"],
                                                            font=customtkinter.CTkFont(size=12))
        self.video_details_label.grid(row=2, column=2, columnspan=2, padx=10, pady=(0,10), sticky="nsw")

        # file size
        self.file_size = customtkinter.CTkLabel(self, text=f"{round(stream_data['file_size'], 1)}MB")
        self.file_size.grid(row=3, column=2, padx=10, pady=10, sticky="nsw")

        # open button
        self.open_button = customtkinter.CTkButton(self, text="Open", command=self.open_file)
        self.open_button.grid(row=3, column=3, columnspan=2, padx=10, pady=10, sticky="nsw")
        HelpTip(downloadPages, self.open_button, message="Open And Play The File")

        self.select_combine = customtkinter.CTkCheckBox(self, width=10, text="", command=self.select_combine_event)
        self.select_help_tip = None

        if CombineManager.is_combine_mode:
            self.select_combine.grid(row=2, column=0, padx=(10,0), sticky="nsew")
            self.set_checkbox()

        # delete button
        self.delete_button = customtkinter.CTkButton(self, text="", fg_color = "transparent", hover_color=HOVER_COLOR,width=15, command=self.delete_event, anchor="center", image=self.assets.delete_icon)
        self.delete_button.grid(row=1, column=4, padx=10, pady=10, sticky="e")
        HelpTip(downloadPages, self.delete_button, message="Delete File")

        self.dialog = None

    
    def open_file(self) -> None:
        try:
            os.startfile(self.file_path)
        except AttributeError:
            subprocess.call(['open', self.file_path])
    
    def delete_event(self) -> None:
        if self.dialog is None or not self.dialog.winfo_exists():
            self.dialog = AlertDialog(self.delete_file, "You are about to delete a file", "You are about to delete this file:\n"+ f"{self.stream_data['title']}\n" + self.stream_data["details"]) 
        else:
            self.dialog.focus()
        

    def delete_file(self) -> None:
        DownloadManager.delete_download(self.stream_data)
        self.downloadPages.remove_element((self.stream_data))

    def select_combine_event(self) -> None:
        if self.select_combine.get():
            self.select_combine_checked()
        else:
            self.select_combine_unchecked()

        self.downloadPages.refresh_checked()

    def select_combine_checked(self) -> None:
        if CombineManager.amount_selected == 0:
            CombineManager.title_selected = self.stream_data["title"]
            if "Audio" in self.stream_data["details"]:
                CombineManager.is_audio_selected=True
            else:
                CombineManager.is_video_selected=True

        CombineManager.amount_selected += 1
        CombineManager.videos_selected.append(self.stream_data)

    def select_combine_unchecked(self) -> None:
        CombineManager.amount_selected -= 1
        if "Audio" in self.stream_data["details"]:
            CombineManager.is_audio_selected=False
        else:
            CombineManager.is_video_selected=False

        CombineManager.videos_selected.remove(self.stream_data)

    def set_checkbox(self) -> None:
        # select for combine mode
        self.select_combine.configure(state="normal")
        
        if self.select_help_tip is not None:
            self.select_help_tip.destroy()
            self.select_combine.unbind("<Enter>")
            self.select_combine.unbind("<Leave>")
            self.select_combine.unbind("<Motion>")
            self.select_combine.unbind("<ButtonPress>")
        
        if self.stream_data in CombineManager.videos_selected:
            self.select_combine.select()
            self.select_help_tip  = HelpTip(self.downloadPages, self.select_combine, message="Deselect This File")
        else: 
            self.select_combine.deselect()

            # enabling selection only for possible combine (same title one audio one audio)
            if "Only" not in self.stream_data["details"] or CombineManager.amount_selected == 2:
                self.select_combine.configure(state="disabled")
                self.select_help_tip  = HelpTip(self.downloadPages, self.select_combine, message="Unable To Choose (2 Downloads Already Chosen or Unsupported Type)")
            
            elif CombineManager.amount_selected == 1 and CombineManager.is_audio_selected and "Video" not in self.stream_data["details"]:
                self.select_combine.configure(state="disabled")
                self.select_help_tip = HelpTip(self.downloadPages, self.select_combine, message="Unable To Choose (Audio File already chosen, choose Video File")

            elif CombineManager.amount_selected == 1 and CombineManager.is_video_selected and "Audio" not in self.stream_data["details"]:
                self.select_combine.configure(state="disabled")
                self.select_help_tip = HelpTip(self.downloadPages, self.select_combine, message="Unable To Choose (Video File already chosen, choose Audio File")

            elif CombineManager.amount_selected == 1 and not CombineManager.title_selected == self.stream_data["title"]:
                self.select_combine.configure(state="disabled")
                self.select_help_tip = HelpTip(self.downloadPages, self.select_combine, message="Unable To Choose (Not The Same YouTube Video as The Other Chosen File)")
            
            else:
                self.select_help_tip = HelpTip(self.downloadPages, self.select_combine, message="Select This File to Combine")


    def toggle_combine_mode(self, mode) -> None:
        if mode:
            self.select_combine.grid(row=2, column=0, padx=(10,0), sticky="nsew")
            self.set_checkbox()
        else:
            self.select_combine.grid_forget()

    def refresh_checked(self) -> None:
        self.set_checkbox()



