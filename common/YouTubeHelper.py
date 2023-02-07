from pytube import Stream
from datetime import datetime
from PIL import Image
from urllib.request import urlopen

class YouTubeHelper():

    @staticmethod
    def views_format(views:int) -> str:
        if(views< 10**3):
            return f"{views}"

        if(views/10**3 < 1000):
            views = views/10**3
            views =  round(views) if views > 10 else round(views,1) 
            return f"{views}K" 

        if(views/10**6 < 1000):
            views = views/10**6
            views =  round(views) if views > 10 else round(views,1) 
            return f"{views}M"

        views = views/10**9
        views =  round(views) if views > 10 else round(views,1) 
        return f"{views}B"

    @staticmethod
    def duration_format(seconds:int) -> str:
        second = seconds%60
        minuts = seconds//60
        hours = seconds//3600
        if(hours > 0):
            return "%02d:%02d:%02d" % (hours, minuts, second)
        return "%02d:%02d" % (minuts, second)

    @staticmethod
    def date_format(date:datetime) -> str:
        arr = str(date).split("-")
        year = arr[0][2:]
        month = arr[1]
        day = arr[2][:2]
        return f"{day}-{month}-{year}"

    @staticmethod
    def filter_streams(streams:list[Stream] ,**kwargs) -> list[Stream]:
        filttered_streams: list[Stream] = []
        for stream in streams:
            if stream.type == "video":
                if not YouTubeHelper.is_valid_key(stream.resolution, "res", **kwargs):
                    continue
            else: # audio
                if not YouTubeHelper.is_valid_key(stream.abr, "res", **kwargs):
                    continue
            if stream.type == "video" and not YouTubeHelper.is_valid_key(stream.fps, "fps", **kwargs):
                continue
            if not YouTubeHelper.is_valid_key(stream.is_progressive, "progressive", **kwargs):
                continue
            if not YouTubeHelper.is_valid_key(stream.type, "type", **kwargs):
                continue
            if not YouTubeHelper.is_valid_key(stream.subtype, "format", **kwargs):
                continue
            filttered_streams.append(stream)
        return filttered_streams

    @staticmethod 
    def is_valid_key(stream_value:any, key: str, **kwargs) -> bool:
        if key not in kwargs.keys():
            return True
        return True if kwargs[key] == stream_value else False

    @staticmethod
    def get_filter_values(streams:list[Stream], key:str,) -> list[str]:
        filter_values:list[str] = []
        for stream in streams:
            if(key == "res"):
                if(stream.type == "video" and stream.resolution not in filter_values):
                    filter_values.append(stream.resolution)
                elif stream.type == "audio" and stream.abr not in filter_values: 
                    filter_values.append(stream.abr)
            if(key == "fps" and stream.fps not in filter_values):
                filter_values.append(f"{stream.fps}")
            if(key == "format" and stream.subtype not in filter_values):
                filter_values.append(stream.subtype)
            if(key == "type" and f"{stream.type.title()} Only" not in filter_values):
                if "Video" not in filter_values and stream.is_progressive:
                    filter_values.append("Video")
                filter_values.append(f"{stream.type.title()} Only")
        return filter_values

    @staticmethod
    def get_cropped_thumbnail(thumbnail:str) -> Image:
        cropped:Image = Image.open(urlopen(thumbnail)).crop((0,60,640,420))
        return cropped
            

