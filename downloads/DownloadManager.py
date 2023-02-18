import json
import os
from customtkinter import CTkFrame
from pytube import Stream
from pprint import pprint

DOWNLOAD_FILE = os.path.join("downloads", "downloads.json")

class DownloadManager():

    @classmethod
    def setDownloads(cls, download_frame:CTkFrame) -> None:
        try:
            with open(DOWNLOAD_FILE, "r") as file:
                data = json.load(file)
                for index, stream_data in data["Downloads"].items():
                    cls.addToCompleted(download_frame, stream_data)
        # check if a file not found (making new dictionary and will make new file when writing)
        except FileNotFoundError as e:
            data = {"index": 1, "Downloads": {}}
            jsonFormat = json.dumps(data, indent=4)
            with open(DOWNLOAD_FILE, "w") as file:
                file.write(jsonFormat)
    
    @classmethod
    def addToCompleted(cls, download_frame, stream_data: dict) -> None:
        download_frame.add_to_completed_downloads(stream_data)

    @classmethod
    def saveToCompleted(cls, stream_data: dict) -> None:
        # opening the download file
        with open(DOWNLOAD_FILE, "r") as file:
            data = json.load(file)

        # adding the download stream
        data["index"] = data["index"]+1
        data["Downloads"][data["index"]] = stream_data

        # writing to the download file
        jsonFormat = json.dumps(data, indent=4)
        with open(DOWNLOAD_FILE, "w") as file:
            file.write(jsonFormat)

    @classmethod 
    def delete_download(cls, stream_data: dict) -> None:
        pprint(stream_data)
        # opening the download file
        with open(DOWNLOAD_FILE, "r") as file:
            data = json.load(file)

        # deleting the download stream save
        index:int = None
        for key in data["Downloads"].keys():
            if data["Downloads"][key] == stream_data:
                index = key
                break
        if index is not None:
            del data["Downloads"][index]

        # writing to the download file
        jsonFormat = json.dumps(data, indent=4)
        with open(DOWNLOAD_FILE, "w") as file:
            file.write(jsonFormat)

        # deleting the file from the pc
        try:
            os.remove(stream_data["file_path"])
        except FileNotFoundError:
            print("File not found")
    
    @classmethod
    def is_already_exist(cls, stream_data:dict) -> bool:
        with open(DOWNLOAD_FILE, "r") as file:
            data = json.load(file)

        # deleting the download stream save
        index:int = None
        for key in data["Downloads"].keys():
            stream_data["file_path"] = data["Downloads"][key]["file_path"]
            stream_data["thumbnail"] = data["Downloads"][key]["thumbnail"]
            if data["Downloads"][key] == stream_data:
                return True

        return False
