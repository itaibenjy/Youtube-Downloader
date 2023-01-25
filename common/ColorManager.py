import customtkinter

class ColorManager():
    appearance_mode: int = 0

    @classmethod
    def setAppearanceMode(cls, mode:str):
        customtkinter.set_appearance_mode(mode)
        actual = customtkinter.get_appearance_mode()
        if(actual == "Dark"):
            cls.appearance_mode = 1;
        elif(actual == "Light"): 
            cls.appearance_mode = 0;
    
    
    @classmethod
    def setTheme(cls, theme:str):
        customtkinter.set_default_color_theme(theme)

    def getColor(self, ctkWidget, attribute:str):
        return ctkWidget.cget(attribute)[self.appearance_mode]
