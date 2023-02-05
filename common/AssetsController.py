import customtkinter
from PIL import Image
import os

class NavigatorAssets():

    def __init__(self) -> None:
        # path to the images directory
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "assets" , "images")

        # icon dimensions
        self.icon_dimensions:tuple = (45,45)

        # initialize all the images
        #self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.search_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "search-light.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "search-dark.png")), size=self.icon_dimensions)
        self.url_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "url-light.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "url-dark.png")), size=self.icon_dimensions)
        self.download_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "download-light.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "download-dark.png")), size=self.icon_dimensions)
        self.settings_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "settings-light.png")),
                                                     dark_image=Image.open(os.path.join(self.image_path, "settings-dark.png")), size=self.icon_dimensions)
        self.logo_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "logo-light.png")),
                                                     dark_image=Image.open(os.path.join(self.image_path, "logo-dark.png")), size=self.icon_dimensions)

class DownloadAssets():

    def __init__(self) -> None:
        # path to the images directory
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, "assets" , "images")

        # icon dimensions
        self.icon_dimensions:tuple = (13,16)

        # initialize all the images
        self.delete_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.image_path, "delete-light.png")),
                                                 dark_image=Image.open(os.path.join(self.image_path, "delete-dark.png")), size=self.icon_dimensions)