import customtkinter 
import tkinter as tk

# put all elements in the scrollable_frame
class ScrollableFrame(customtkinter.CTkFrame):

    def __init__(self, frame):
        super().__init__(frame, bg_color="transparent")
        self.canvas = tk.Canvas(self, bg=frame["bg"], highlightthickness=0)
        scrollbar = customtkinter.CTkScrollbar(self, command=self.canvas.yview)
        self.scrollable_frame = customtkinter.CTkFrame(self.canvas, bg_color="transparent", width=700)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        #setup MouseWheel
        self._setup_mousewheel(frame, self.canvas)
        
        self.update()

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw", width=900)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(column=1, row=1, sticky="ns")
        scrollbar.grid(column=2,row=1, sticky="nse")




    def _setup_mousewheel(self,frame,canvas):
        frame.bind('<Enter>', lambda *args, passed=canvas: self._bound_to_mousewheel(*args,passed))
        #frame.bind('<Leave>', lambda *args, passed=canvas: self._unbound_to_mousewheel(*args,passed))

    def _bound_to_mousewheel(self,event, canvas):
        canvas.bind_all("<MouseWheel>", lambda *args, passed=canvas: self._on_mousewheel(*args,passed))

    def _unbound_to_mousewheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
    
    def update(self):
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )



