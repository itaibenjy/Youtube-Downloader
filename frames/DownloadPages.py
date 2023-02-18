import customtkinter
from frames.DownloadVideoFrame import DownloadVideoFrame
from frames.CompletedVideoFrame import CompletedVideoFrame
from PIL import Image


class DownloadPages(customtkinter.CTkScrollableFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.current_tabs_count = 0
        self.grid_columnconfigure(1, weight=1)

        self.elements = []
        self.rendered_elements = []

    def add_element(self, element) -> None:
        self.elements.insert(0,element)
        self.rerender_elements()
    
    def remove_element(self, element) -> str:
        thumbnail:str = None
        for elem in self.elements:
            if elem[0] == element:
                self.elements.remove(elem)
                try:
                    thumbnail = elem[1]
                except IndexError:
                    pass
        self.rerender_elements()
        return thumbnail

    def rerender_elements(self):
        # clearing all data
        for i in range(len(self.rendered_elements)):
            self.rendered_elements[i].destroy()
        for i in range(0,self.current_tabs_count,1):
            self.delete(f"{i+1}")
        self.current_tabs_count=0

        current_row = 0  
        
        for i in range(len(self.elements)):
            if len(self.elements[i]) == 2: 
                new_video_frame = DownloadVideoFrame(self, self.elements[i][0], self.elements[i][1])
            elif len(self.elements[i]) == 1:
                new_video_frame = CompletedVideoFrame(self, self.elements[i][0])
            self.rendered_elements.append(new_video_frame)
            new_video_frame.grid(row = current_row, column=1, padx=20, pady=10, sticky="nswe")
            current_row += 1

    def download_progress(self, stream, progress:float, percent:int):
        for element in self.rendered_elements:
            if element.stream.itag == stream.itag and element.stream.title == stream.title:
                element.progress_update(progress, percent)
                return
    
    def toggle_combine_mode(self, mode:bool) -> None:
        for element in self.rendered_elements:
            element.toggle_combine_mode(mode)


        
