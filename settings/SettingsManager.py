import json 
import os
from common.ColorManager import ColorManager
   
SETTINGS_FILE = os.path.join("settings", "settings.json")
DEFAULT_THEME = "red"
DEFAULT_APPEARANCE = "Dark"
DEFAULT_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)))

class SettingsManager():
    
    theme = ""
    appearance = ""
    download_folder = ""

    @classmethod
    def setAppearance(cls, mode:str) -> None:
        cls.setValue("appearance", mode)
        cls.appearance = mode
        ColorManager.setAppearanceMode(cls.appearance)

    @classmethod
    def setTheme(cls, theme:str) -> None:
        theme_location = os.path.join("assets", "themes",f"{theme}.json")
        cls.setValue("theme", theme)
        cls.theme = theme
        ColorManager.setTheme(theme_location)

    @classmethod
    def setFolder(cls, download_folder:str) -> None:
        cls.setValue("folder", download_folder)
        cls.download_folder = download_folder

    @classmethod
    def setValue(cls, attribute:str, value) -> None:
        with open(SETTINGS_FILE, "r") as file:
            data = json.load(file)

        data[attribute] = value
        jsonFormat = json.dumps(data, indent=4)

        with open(SETTINGS_FILE, "w") as file:
            file.write(jsonFormat)

    @classmethod
    def setSettings(cls) -> None:
        try:
            with open(SETTINGS_FILE, "r") as file:
                data = json.load(file)
                cls.appearance = data.get("appearance")
                cls.theme = data.get("theme")
                cls.download_folder = data.get("folder")
        # check if a file not found (making new dictionary and will make new file when writing)
        except FileNotFoundError as e:
            data = {}
        
        cls.checkDefaults(data)
        jsonFormat = json.dumps(data, indent=4)
        with open(SETTINGS_FILE, "w") as file:
            file.write(jsonFormat)

        theme_location = os.path.join("assets", "themes",f"{cls.theme}.json")
        ColorManager.setAppearanceMode(cls.appearance)
        ColorManager.setTheme(theme_location)

    # setting default parameters in case file was tempered with 
    @classmethod
    def checkDefaults(cls, data)-> None:

        if(cls.appearance is None or cls.appearance == ""):
            cls.appearance = DEFAULT_APPEARANCE
            data["appearance"] = cls.appearance
        if(cls.theme is None or cls.theme== ""):
            cls.theme= DEFAULT_THEME
            data["theme"] = cls.theme
        if(cls.download_folder is None or cls.download_folder== ""):
            cls.download_folder = DEFAULT_FOLDER
            data["folder"] = cls.download_folder








