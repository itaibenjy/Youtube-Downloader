from pytube import Stream

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
    def filter_streams(streams:list[Stream] ,**kwargs) -> list[Stream]:
        filttered_streams: list[Stream] = []
        for stream in streams:
            if not YouTubeHelper.is_valid_key(stream.res, "res", **kwargs):
                break
            if not YouTubeHelper.is_valid_key(stream.fps, "fps", **kwargs):
                break
            if not YouTubeHelper.is_valid_key(stream.progressive, "progressive", **kwargs):
                break
            if not YouTubeHelper.is_valid_key(stream.mime_type, "mime_type", **kwargs):
                break
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
            if(key == "res" and stream.res not in filter_values):
                filter_values.append(stream.res)
            if(key == "fps" and stream.fps not in filter_values):
                filter_values.append(stream.fps)
            if(key == "progressive" and stream.progressive not in filter_values):
                filter_values.append(stream.progressive)
            if(key == "mime_type" and stream.mime_type not in filter_values):
                filter_values.append(stream.mime_type)
        return filter_values


        

