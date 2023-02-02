import customtkinter
from frames.DownloadVideoFrame import DownloadVideoFrame
from frames.CompletedVideoFrame import CompletedVideoFrame
from PIL import Image


class DownloadPages(customtkinter.CTkTabview):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.current_tabs_count = 0

        self.elements = []
        self.rendered_elements = []

    def add_element(self, element) -> None:
        self.elements.insert(0,element)
        self.rerender_elements()
    
    def remove_element(self, element) -> Image:
        thumbnail:Image = None
        for elem in self.elements:
            if elem[0] == element:
                self.elements.remove(elem)
                thumbnail = elem[1]
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
            # adding tabs when needed
            if current_row % 3 == 0:
                self.add(f"{(current_row//3)+1}")
                self.tab(f"{(current_row//3)+1}").columnconfigure(1, weight=1)
                self.current_tabs_count += 1
            if len(self.elements[i]) == 2: 
                new_video_frame = DownloadVideoFrame(self.tab(f"{(current_row//3)+1}"), self.elements[i][0], self.elements[i][1])
            elif len(self.elements[i]) == 3:
                new_video_frame = CompletedVideoFrame(self.tab(f"{(current_row//3)+1}"), self.elements[i][0], self.elements[i][1], self.elements[i][2])
            self.rendered_elements.append(new_video_frame)
            new_video_frame.grid(row = current_row%3, column=1, padx=20, pady=10, sticky="nswe")
            current_row += 1

    def download_progress(self, stream, progress:float, percent:int):
        for element in self.rendered_elements:
            if element.stream.itag == stream.itag and element.stream.title == stream.title:
                element.progress_update(progress, percent)
                return


        
