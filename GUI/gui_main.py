import os
import threading
import tkinter as tk
from tkinter import ttk
from GUI.gui_edit import gui_edit
from timer import TimerSystem


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-timer")
        self.timer_system = None
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
        ttk.Button(button_frame, text="Stop all timers", command=self.on_stop).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.root, text="Exit", command=self.on_exit).pack(pady=5)

    def on_load(self):
        path = os.path.join(os.getcwd(), "Timers")
        files = os.listdir(path)
        file_names = ''
        for file in files:
            if file.endswith('.json'):
                file_names += file.split('.')[0] + ", "
        self.file_label.config(text=file_names)

    def on_start(self):
        self.file_name_str = self.file_name.get()
        if not self.file_name_str:
            self.file_label.config(text="File name is empty")
            return

        def start_timers():
            try:
                self.timer_system = TimerSystem(self.file_name_str)
                self.timer_system.set_root_window(self.root)  # Передаем главное окно
                self.timer_system.start()
            except Exception as e:
                print(f"Error starting timers: {e}")

        timer_thread = threading.Thread(target=start_timers, daemon=True)
        timer_thread.start()
        self.file_label.config(text="Timers started. Press hotkeys Ctrl+Esc to stop.")

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
                gui_create(on_back_callback=gui, file_name=file_name)
            else:
                self.file_label.config(text="File is already exist")

    def on_edit(self):
        self.file_name_str = self.file_name.get()
        file_name = self.file_name_str
        if file_name == "":
            self.file_label.config(text="File name is empty")
        else:
            if os.path.exists(f"Timers/{file_name}.json"):
                self.root.destroy()
                gui_edit(on_back_callback=gui, file_name=file_name)
            else:
                self.file_label.config(text="File does not exist")

    def on_stop(self):
        """Остановка всех таймеров"""
        if self.timer_system:
            self.timer_system.stop_all()
            self.timer_system = None
            self.file_label.config(text="Все таймеры остановлены")
        else:
            self.file_label.config(text="Система таймеров не запущена")

    def on_exit(self):
        if self.timer_system:
            self.timer_system.stop_all()
        else:
            self.root.destroy()
            os._exit(0)


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
