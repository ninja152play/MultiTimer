import os
import tkinter as tk
from tkinter import ttk
from GUI.gui_edit import gui_edit
from timer import TimerSystem


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-timer")
        self.setup()

    def setup(self):
        ttk.Button(self.root, text="Load file", command=self.on_load).pack(pady=5)
        self.file_label = tk.Label(self.root, text="")
        self.file_label.pack(pady=5)

        ttk.Label(self.root, text="Write file name").pack(pady=5)
        self.file_name = ttk.Entry(self.root, width=40)
        self.file_name.pack(pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Start work", command=self.on_start).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create new timer list", command=self.on_create).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit timer list", command=self.on_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(text="Exit", command=self.on_exit).pack(side=tk.TOP, padx=5)

    def on_load(self):
        path = os.path.join(os.getcwd(), "Timers")
        files = os.listdir(path)
        file_names = ''
        for file in files:
            file_names += file.split('.')[0] + ", "
        self.file_label.config(text=file_names)

    def on_start(self):
        self.file_name_str = self.file_name.get()
        self.root.destroy()
        timer = TimerSystem(self.file_name_str)
        restart = timer.start()
        if restart:
            gui()

    def on_create(self):
        self.file_name_str = self.file_name.get()
        file_name = self.file_name_str
        if file_name == "":
            self.file_label.config(text="File name is empty")
        else:
            if not os.path.exists(f"Timers/{file_name}.json"):
                with open(f"Timers/{file_name}.json", "w") as f:
                    f.write('{"timers": []}')
                self.root.destroy()
                restart = gui_create(on_back_callback=gui, file_name=file_name)
                if restart:
                    gui()
            else:
                self.file_label.config(text="File is already exist")

    def on_edit(self):
        self.file_name_str = self.file_name.get()
        file_name = self.file_name_str
        if file_name == "":
            self.file_label.config(text="File name is empty")
        else:
            self.root.destroy()
            restart = gui_edit(on_back_callback=gui, file_name=file_name)
            if restart:
                gui()

    def on_exit(self):
        self.root.destroy()
        return False


def gui():
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()


class GuiCreate:
    def __init__(self, root, on_back_callback=None, file_name=""):
        self.on_back_callback = on_back_callback
        self.file_name_str = file_name
        self.root = root
        self.root.title("Multi-timer")
        self.setup()

    def setup(self):
        self.file_label = tk.Label(self.root, text=f"File {self.file_name_str} created")
        self.file_label.pack(pady=5)
        ttk.Button(self.root, text="Ok", command=self.on_ok).pack(pady=5)


    def on_ok(self):
        self.root.destroy()
        if self.on_back_callback:
            self.on_back_callback()


def gui_create(on_back_callback=None, file_name=""):
    root = tk.Tk()
    app = GuiCreate(root, on_back_callback=gui, file_name=file_name)
    root.mainloop()

