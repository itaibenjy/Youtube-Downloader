from moviepy.editor import VideoFileClip, AudioFileClip
from proglog import ProgressBarLogger
from downloads.DownloadManager import DownloadManager

class CombineManager():

    is_combine_mode:bool = False
    amount_selected:int = 0
    is_video_selected:bool = False
    is_audio_selected:bool = False
    title_selected:str = None
    videos_selected:list = []

    @classmethod
    def combine_chosen_downloads(cls, completed_pages, progress_label, progress_bar, progress_percentage) -> None:
        video_path:str = None
        audio_path:str = None
        audio_quality:str = None
        for download in cls.videos_selected:
            if "Audio" in download["details"]:
                audio_path = download["file_path"]
                audio_quality = download["details"].split("·")[2]
            else: 
                video_path = download["file_path"]
                new_data = download.copy()


        file_name = video_path[:video_path.find(".")] + "_Combined_" + audio_quality.replace(" ","") + video_path[video_path.find("."):]
        new_data["details"] = new_data["details"].replace("Video Only", "Combined Video Audio") + "  ·" +  audio_quality
        new_data["file_path"] = file_name

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(file_name, logger= MyBarLogger(progress_bar, progress_label, progress_percentage,min_time_interval=1.0))

        DownloadManager.saveToCompleted(new_data)
        completed_pages.add_element([new_data])

class MyBarLogger(ProgressBarLogger):

    def __init__(self, progress_bar, progress_label, progress_percentage, init_state=None, bars=None, ignored_bars=None,
                 logged_bars='all', min_time_interval=0, ignore_bars_under=0):
        super().__init__(init_state, bars=bars, ignored_bars=ignored_bars, logged_bars=logged_bars, min_time_interval=min_time_interval, ignore_bars_under=ignore_bars_under)
        self.progress_bar = progress_bar
        self.label = progress_label
        self.percentage = progress_percentage

    def bars_callback(self, bar, attr, value, old_value=None):
        total = self.bars[bar]['total']
        if bar == "chunk":
            self.label.configure(text = "Adding Audio")
        elif bar == "t":
            self.label.configure(text = "Saving Video")

        percentage = value / total
        self.progress_bar.set(percentage)
        self.percentage.configure(text = f"{round(percentage*100)}%")

