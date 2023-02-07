import customtkinter


class AlertDialog(customtkinter.CTkToplevel):
    def __init__(self, ok_callback, title, message:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x200")
        self.grid_columnconfigure((1,2), weight=1)
        self.title(title)
        self.ok_callback = ok_callback

        self.message_frame = self.get_message(message)
        self.message_frame.grid(row = 1, column = 1, columnspan = 2, padx=20, pady=20, sticky="nswe")

        self.ok_button = customtkinter.CTkButton(self, text="OK", command=self.ok_event)
        self.ok_button.grid(row = 2, column = 2, padx=20, pady=20, sticky="nswe")

        self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.cancel_event)
        self.cancel_button.grid(row = 2, column = 1, padx=20, pady=20, sticky="nswe")


    def get_message(self, message:str) -> customtkinter.CTkFrame:
        lines = message.split("\n")
        message_frame = customtkinter.CTkFrame(self)
        message_frame.grid_columnconfigure(1, weight = 1)
        for index,line in enumerate(lines):
            line_label = customtkinter.CTkLabel(message_frame, text=line)
            line_label.grid(row=index, column=1, pady=2, padx=10, sticky="nswe")
        return message_frame

    def ok_event(self):
        self.ok_callback()
        self.destroy()

    def cancel_event(self):
        self.destroy()



