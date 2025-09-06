import os
import json
import tkinter as tk
from tkinter import ttk
from key_code import getkey


class GuiEdit:
    def __init__(self, root, on_back_callback=None, file_name=""):
        self.file_prefix = file_name
        self.file_name = file_name + ".json"
        self.root = root
        self.root.title("Edit")
        self.on_back_callback = on_back_callback
        self.data = self.load_json(self.file_name)
        self.setup()

    def setup(self):
        self.file_label = tk.Label(self.root, text=self.print_json(self.data))
        self.file_label.pack(pady=5)

        self.error_label = tk.Label(self.root, text="")
        self.file_label.pack(pady=5)

        ttk.Label(self.root, text="Timer Name").pack(pady=5)
        self.timer_name = ttk.Entry(self.root, width=20)
        self.timer_name.pack(pady=5)

        ttk.Label(self.root, text="Timer Interval").pack(pady=5)
        self.timer_interval = ttk.Entry(self.root, width=20)
        self.timer_interval.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Timer Key\nНажмите на кнопку, затем нажмите клавишу")
        self.status_label.pack(pady=5)
        self.bind_button = tk.Button(self.root, text="Назначить клавишу",
                                     command=self.start_key_binding)
        self.bind_button.pack(pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="Add", command=self.on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.on_save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.on_delete).pack(side=tk.TOP, padx=5)
        ttk.Button(text="Back", command=self.on_back).pack(side=tk.TOP, padx=5)

    def start_key_binding(self):
        self.status_label.config(text="Нажмите любую клавишу...")
        self.bind_button.config(state="disabled")

        self.root.bind("<Key>", self.assign_key)
        self.root.focus_set()

    def assign_key(self, event):
        key = event.keysym
        key_code = event.keycode

        self.timer_key = getkey(key_code)
        if self.timer_key is None:
            self.status_label.config(text=f"Эта клавиша не поддерживается: {key}")
        else:
            self.status_label.config(text=f"Назначена клавиша: {key}")

        self.root.unbind("<Key>")
        self.bind_button.config(state="normal")

    def on_add(self):
        timer = {'name': self.timer_name.get(), 'interval': int(self.timer_interval.get()), 'callback': f'{self.timer_name.get()}Callback', 'key': self.timer_key}
        self.data["timers"].append(timer)
        self.save_json(self.data)
        self.root.destroy()
        gui_edit(self.on_back_callback, self.file_prefix)

    def on_save(self):
        name = self.timer_name.get()
        time = self.timer_interval.get()
        try:
            key = self.timer_key
        except:
            pass
        for i, timer in enumerate(self.data["timers"]):
            if timer["name"] == name:
                if time:
                    self.data["timers"][i]["interval"] = int(time)
                try:
                    if key:
                        self.data["timers"][i]["key"] = key
                except:
                    pass
                self.save_json(self.data)
                self.root.destroy()
                gui_edit(self.on_back_callback, self.file_prefix)

    def on_delete(self):
        name = self.timer_name.get()
        for timer in self.data["timers"]:
            if timer["name"] == name:
                self.data["timers"].remove(timer)
                self.save_json(self.data)
                self.root.destroy()
                gui_edit(self.on_back_callback, self.file_prefix)

    def on_back(self):
        self.root.destroy()
        if self.on_back_callback:
            self.on_back_callback()

    def load_json(self, file_name: str):
        if file_name:
            try:
                with open(f"Timers/{file_name}", "r") as f:
                    return json.load(f)
            except:
                return {}
        else:
            return "No timer selected"

    def print_json(self, data):
        if data:
            answer = ""
            for timer in data["timers"]:
                answer += f"Name: {timer['name']}\n Time: {timer['interval']}\n Key: {timer['key']}\n\n"
            return answer

        else:
            return "No timer selected"

    def save_json(self, data):
        if data:
            with open(f"Timers/{self.file_name}", "w") as f:
                json.dump(data, f)


def gui_edit(on_back_callback=None, file_name=""):
    root = tk.Tk()
    app = GuiEdit(root, on_back_callback, file_name)
    root.mainloop()