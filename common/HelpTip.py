from tktooltip import ToolTip
import customtkinter
from common.ColorManager import ColorManager


class HelpTip():
    def __init__(self, app, button, message:str, follow=True) -> None:

        self.color = ColorManager()
        self.background = self.color.getColor(app, "fg_color")
        self.text_color = self.border_color = self.color.getColor(button, "text_color")

        ToolTip(button, msg=message, follow = follow, delay=0.3, fg= self.text_color,
         bg = self.background, x_offset= +20, y_offset= +5, parent_kwargs={"bg": self.border_color, "padx": 1, "pady": 1})
    