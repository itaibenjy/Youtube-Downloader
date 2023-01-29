import customtkinter 
import tkinter as tk

# put all elements in the scrollable_frame
class ScrollableFrame(customtkinter.CTkFrame):

    def __init__(self, frame):
        super().__init__(frame, bg_color="transparent")
        canvas = tk.Canvas(self, bg=frame["bg"], highlightthickness=0)
        scrollbar = customtkinter.CTkScrollbar(self, command=canvas.yview)
        self.scrollable_frame = customtkinter.CTkFrame(canvas, bg_color="transparent")

        #setup MouseWheel
        self._setup_mousewheel(self.scrollable_frame, canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")




    def _setup_mousewheel(self,frame,canvas):
        frame.bind('<Enter>', lambda *args, passed=canvas: self._bound_to_mousewheel(*args,passed))
        frame.bind('<Leave>', lambda *args, passed=canvas: self._unbound_to_mousewheel(*args,passed))

    def _bound_to_mousewheel(self,event, canvas):
        canvas.bind_all("<MouseWheel>", lambda *args, passed=canvas: self._on_mousewheel(*args,passed))

    def _unbound_to_mousewheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta)), "units")




