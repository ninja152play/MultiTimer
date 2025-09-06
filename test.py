import tkinter as tk
from tkinter import messagebox


class KeyBinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Назначение клавиш")
        self.root.geometry("400x300")

        # Словарь для хранения назначенных клавиш
        self.key_bindings = {}

        self.create_widgets()

    def create_widgets(self):
        # Поле для отображения текущей привязки
        self.status_label = tk.Label(self.root, text="Нажмите на кнопку, затем нажмите клавишу",
                                     font=("Arial", 12))
        self.status_label.pack(pady=20)

        # Кнопка для назначения клавиши
        self.bind_button = tk.Button(self.root, text="Назначить клавишу",
                                     command=self.start_key_binding,
                                     font=("Arial", 14), height=2)
        self.bind_button.pack(pady=10)

        # Поле для отображения назначенных клавиш
        self.bindings_text = tk.Text(self.root, height=10, width=40)
        self.bindings_text.pack(pady=10, padx=20)

        # Кнопка очистки
        self.clear_button = tk.Button(self.root, text="Очистить",
                                      command=self.clear_bindings)
        self.clear_button.pack(pady=5)

    def start_key_binding(self):
        self.status_label.config(text="Нажмите любую клавишу...")
        self.bind_button.config(state="disabled")

        # Привязываем обработчик клавиш ко всему окну
        self.root.bind("<Key>", self.assign_key)
        self.root.focus_set()  # Устанавливаем фокус на окно

    def assign_key(self, event):
        # Получаем нажатую клавишу
        key = event.keysym
        key_code = event.keycode

        # Сохраняем привязку
        self.key_bindings[key] = key_code

        # Обновляем интерфейс
        self.status_label.config(text=f"Назначена клавиша: {key}")
        self.update_bindings_display()

        # Отвязываем обработчик и восстанавливаем кнопку
        self.root.unbind("<Key>")
        self.bind_button.config(state="normal")

    def update_bindings_display(self):
        self.bindings_text.delete(1.0, tk.END)
        for key, code in self.key_bindings.items():
            self.bindings_text.insert(tk.END, f"Клавиша: {key} (код: {code})\n")

    def clear_bindings(self):
        self.key_bindings.clear()
        self.update_bindings_display()
        self.status_label.config(text="Привязки очищены")


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyBinderApp(root)
    root.mainloop()