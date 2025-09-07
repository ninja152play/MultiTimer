import json
import os
import time
import threading
import keyboard
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any
from key_code import getkey


class TimerSystem:
    def __init__(self, config_file: str = "timers_config.json"):
        self.config_file = config_file if config_file.endswith(".json") else config_file + ".json"
        self.data = self.load_config()
        self.active_timers: Dict[str, threading.Timer] = {}
        self.timer_end_times: Dict[str, datetime] = {}
        self.status_window = None
        self.status_labels = {}
        self.root = None
        self.running = True
        self.keyboard_thread = None

        print("Загружена конфигурация таймеров:")
        for timer in self.data.get("timers", []):
            print(f"  {timer['name']}: {timer['interval']}ms, клавиша '{timer['key']}'")

    def set_root_window(self, root):
        """Устанавливает главное окно Tkinter"""
        self.root = root

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(f"Timers/{self.config_file}", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл {self.config_file} не найден")
            return {"timers": []}
        except json.JSONDecodeError:
            print(f"Ошибка чтения JSON файла {self.config_file}")
            return {"timers": []}

    def start_timer(self, timer_name: str):
        """Запускает таймер по имени"""
        timer_config = None
        for timer in self.data.get("timers", []):
            if timer["name"] == timer_name:
                timer_config = timer
                break

        if not timer_config:
            print(f"Таймер {timer_name} не найден в конфигурации")
            return

        if timer_name in self.active_timers:
            print(f"Таймер {timer_name} уже запущен")
            self.stop_timer(timer_name)


        end_time = datetime.now() + timedelta(seconds=timer_config["interval"])
        self.timer_end_times[timer_name] = end_time

        def timer_callback():
            print(f"⏰ ТАЙМЕР '{timer_name}' ЗАВЕРШЕН! Время: {datetime.now().strftime('%H:%M:%S')}")

            # Показываем GUI уведомление
            self.show_timeout_notification(timer_name)

            # Удаляем из активных таймеров
            if timer_name in self.active_timers:
                del self.active_timers[timer_name]
            if timer_name in self.timer_end_times:
                del self.timer_end_times[timer_name]

            # Обновляем окно статуса
            self.safe_update_status_window()

        interval_seconds = timer_config["interval"]
        self.active_timers[timer_name] = threading.Timer(interval_seconds, timer_callback)
        self.active_timers[timer_name].start()

        print(f"▶️ Запущен таймер '{timer_name}' на {interval_seconds / 60:.1f} минут")
        print(f"   Завершится в: {end_time.strftime('%H:%M:%S')}")

        # Показываем окно статуса
        self.safe_show_status_window()

    def stop_timer(self, timer_name: str):
        """Останавливает таймер"""
        if timer_name in self.active_timers:
            restart = "_restart_" + timer_name
            if restart in self.active_timers:
                self.active_timers.pop(restart)
            self.active_timers[timer_name].cancel()
            del self.active_timers[timer_name]
            if timer_name in self.timer_end_times:
                del self.timer_end_times[timer_name]

            print(f"⏹️ Таймер '{timer_name}' остановлен")

            # Обновляем окно статуса
            self.safe_update_status_window()
        else:
            print(f"Таймер '{timer_name}' не активен")

    def safe_show_status_window(self):
        """Безопасно показывает окно статуса"""
        if self.root:
            self.root.after(0, self.show_status_window)

    def safe_update_status_window(self):
        """Безопасно обновляет окно статуса"""
        if self.root:
            self.root.after(0, self.update_status_window)

    def show_status_window(self):
        """Показывает окно с статусом таймеров"""
        if self.status_window is None or not self.status_window.winfo_exists():
            self.create_status_window()

    def create_status_window(self):
        """Создает окно статуса"""
        if self.status_window is not None and self.status_window.winfo_exists():
            return

        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Статус таймеров")
        self.status_window.geometry("400x350")
        self.status_window.resizable(False, True)
        self.status_window.attributes('-topmost', True)

        # Заголовок
        title_label = tk.Label(self.status_window, text="⏰ АКТИВНЫЕ ТАЙМЕРЫ",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Фрейм для таймеров
        timer_frame = tk.Frame(self.status_window)
        timer_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.status_labels = {}

        # Создаем метки для каждого таймера из конфига
        for timer in self.data.get("timers", []):
            timer_name = timer["name"]
            key = timer["key"]

            timer_row = tk.Frame(timer_frame)
            timer_row.pack(fill=tk.X, pady=5)

            # Информация о таймере
            info_label = tk.Label(timer_row, text=f"{key} → {timer_name}",
                                  font=("Arial", 10), anchor="w")
            info_label.pack(side=tk.LEFT, padx=(0, 10))

            # Метка для отображения времени
            time_label = tk.Label(timer_row, text="не активен",
                                  font=("Arial", 10, "bold"),
                                  fg="red", width=15)
            time_label.pack(side=tk.RIGHT)

            self.status_labels[timer_name] = time_label

        # Кнопка закрытия
        close_btn = ttk.Button(self.status_window, text="Закрыть",
                               command=self.close_status_window)
        close_btn.pack(pady=10)

        # Запускаем обновление времени
        self.start_status_updates()

    def start_status_updates(self):
        """Запускает периодическое обновление статуса"""

        def update_loop():
            if self.status_window and self.status_window.winfo_exists():
                self.update_status_window()
                self.root.after(1000, update_loop)

        if self.root:
            self.root.after(1000, update_loop)

    def update_status_window(self):
        """Обновляет время в окне статуса"""
        if self.status_window is None or not self.status_window.winfo_exists() or not self.status_labels:
            return

        current_time = datetime.now()

        for timer_name, label in self.status_labels.items():
            if timer_name in self.timer_end_times:
                end_time = self.timer_end_times[timer_name]
                remaining = end_time - current_time

                if remaining.total_seconds() > 0:
                    mins, secs = divmod(int(remaining.total_seconds()), 60)
                    label.config(text=f"{mins:02d}:{secs:02d}", fg="green")
                else:
                    label.config(text="завершен", fg="blue")
            else:
                label.config(text="не активен", fg="red")

    def close_status_window(self):
        """Закрывает окно статуса"""
        if self.status_window and self.status_window.winfo_exists():
            self.status_window.destroy()
            self.status_window = None

    def show_timeout_notification(self, timer_name: str):
        """Показывает уведомление о завершении таймера"""
        if self.root:
            self.root.after(0, lambda: self.create_timeout_window(timer_name))

    def create_timeout_window(self, timer_name: str):
        """Создает окно уведомления о завершении таймера"""
        timeout_window = tk.Toplevel(self.root)
        timeout_window.title("Таймер завершен")
        timeout_window.geometry("300x250")
        timeout_window.resizable(False, False)
        timeout_window.attributes('-topmost', True)

        # Центрируем окно
        timeout_window.update_idletasks()
        x = (timeout_window.winfo_screenwidth() - timeout_window.winfo_width()) // 2
        y = (timeout_window.winfo_screenheight() - timeout_window.winfo_height()) // 2
        timeout_window.geometry(f"+{x}+{y}")

        file_label = tk.Label(timeout_window,
                              text=f"⏰ Таймер '{timer_name}' завершен!",
                              font=("Arial", 14),
                              wraplength=250)
        file_label.pack(pady=20)

        current_time = datetime.now().strftime("%H:%M:%S")
        time_label = tk.Label(timeout_window,
                              text=f"Время: {current_time}",
                              font=("Arial", 10))
        time_label.pack(pady=5)

        ttk.Button(timeout_window, text="OK",
                   command=timeout_window.destroy, width=15).pack(pady=10)

        # Звуковой сигнал
        timeout_window.bell()

    def setup_keyboard_hotkeys(self):
        """Настраивает горячие клавиши для запуска таймеров"""
        print("\nНастройка горячих клавиш...")

        for timer in self.data.get("timers", []):
            key = timer["key"]
            name = timer["name"]

            def create_callback(timer_name=name):
                def callback():
                    print(f"\n🎯 Нажата клавиша {key} - запуск таймера '{timer_name}'")
                    self.start_timer(timer_name)

                return callback

            keyboard.add_hotkey(key, create_callback())
            print(f"  {key} → {name}")

    def start(self):
        """Запускает систему таймеров"""
        print("🚀 Система таймеров запущена!")
        print("Нажмите Ctrl+Esc для выхода")
        print("Доступные клавиши:")

        for timer in self.data.get("timers", []):
            print(f"  {timer['key']} - {timer['name']} ({timer['interval']} сек)")

        self.setup_keyboard_hotkeys()

        def keyboard_wait():
            try:
                keyboard.wait('ctrl+esc')
            except:
                pass
            finally:
                self.running = False
                self.stop_all()

        self.keyboard_thread = threading.Thread(target=keyboard_wait, daemon=True)
        self.keyboard_thread.start()
        return True

    def stop_all(self):
        """Останавливает все таймеры"""
        print("\n🛑 Остановка всех таймеров...")
        for timer_name in list(self.active_timers.keys()):
            if timer_name.startswith("_restart_"):
                continue
            self.stop_timer(timer_name)
        if self.status_window and self.status_window.winfo_exists():
            self.status_window.destroy()
        try:
            keyboard.unhook_all()
        except:
            pass
        print("Все таймеры остановлены")
