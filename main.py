from os.path import ismount
import tkinter
import customtkinter
from nav_frame import NavigatorFrame
 
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

HEIGHT: int = 1100 
WIDTH: int = 700

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Youtube Downloader")
        self.geometry(f"{HEIGHT}x{WIDTH}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.nav_frame = NavigatorFrame(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
