
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

