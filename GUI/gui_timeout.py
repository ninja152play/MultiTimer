import tkinter as tk
from tkinter import ttk
from datetime import datetime


class GuiTimeout:
    def __init__(self, root, timer_name=""):
        self.timer_name = timer_name
        self.root = root
        self.root.title("Timeout Notification")
        self.root.geometry("300x250")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        self.root.lift()
        self.setup()

    def setup(self):
        # Центрируем окно
        self.root.eval('tk::PlaceWindow . center')

        self.file_label = tk.Label(self.root,
                                   text=f"⏰ Таймер '{self.timer_name}' завершен!",
                                   font=("Arial", 14),
                                   wraplength=250)
        self.file_label.pack(pady=20)

        current_time = datetime.now().strftime("%H:%M:%S")
        time_label = tk.Label(self.root,
                              text=f"Время: {current_time}",
                              font=("Arial", 10))
        time_label.pack(pady=5)

        ttk.Button(self.root, text="OK", command=self.on_ok, width=15).pack(pady=10)

    def on_ok(self):
        self.root.destroy()


def gui_timeout(timer_name=""):
    root = tk.Tk()
    app = GuiTimeout(root, timer_name=timer_name)
    root.mainloop()