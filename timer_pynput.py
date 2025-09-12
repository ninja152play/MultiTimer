import json
import logging
import re
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
from pynput import keyboard
from key_code import getkey


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TimerSystem:
    def __init__(self, config_file: str = "timers_config.json"):
        self.config_file = Path("Timers") / config_file
        if not self.config_file.suffix == ".json":
            self.config_file = self.config_file.with_suffix(".json")
        self.STOP_KEY: Dict = {"ctrl_l": 0}
        self.data: Dict = self._load_config()
        self._print_config()

        self.active_timers: Dict[str, threading.Timer] = {}
        self.timer_end_times: Dict[str, datetime] = {}

        self.root: Optional[tk.Tk] = None
        self.status_window: Optional[tk.Toplevel] = None
        self.status_labels: Dict[str, tk.Label] = {}

        self.running: bool = True
        self.keyboard_thread: Optional[threading.Thread] = None

    def _load_config(self) -> Dict:
        """Загрузка конфигурации из JSON файла"""
        try:
            if not self.config_file.exists():
                logger.warning(f"Файл конфигурации {self.config_file} не найден")
                return {"timers": []}

            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Конфигурация загружена из {self.config_file}")
                return data

        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return {"timers": []}
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            return {"timers": []}

    def _print_config(self):
        if self.data:
            logger.info("Таймеры:")
            for timer in self.data["timers"]:
                logger.info(f"{timer['name']}: {timer['interval']} --> {timer['key']}")
        else:
            logger.info("Нет таймеров.")

    def __on_press(self, key):
        try:
            key_name = key.char
        except:
            try:
                key_name = key._name_
            except:
                logger.warning("Неизвестная клавиша")
        try:
            key_code = key.vk
        except:
            try:
                key_code = key._value_
            except:
                logger.warning("Неизвестная клавиша")
        logger.info(f"Нажата клавиша: {key_name} ({key_code})")

        if str(key_name) == "ctrl_l" or str(key_name) == "esc":
            if str(key_name) == "esc":
                if self.STOP_KEY["ctrl_l"] == 1:
                    self.stop()
            if str(key_name) == "ctrl_l":
                if self.STOP_KEY["ctrl_l"] != 1:
                    self.STOP_KEY["ctrl_l"] = 1
                else:
                    self.STOP_KEY = {"ctrl_l": 0}
        else:
            self.STOP_KEY = {"ctrl_l": 0}

        if isinstance(key_code, int):
            pressed_key = getkey(key_code)
            logger.info(f"Нажата клавиша: {pressed_key}")
        else:
            try:
                key_code = re.sub(r'[<>]', '', str(key_code))
                print(key_code)
                pressed_key = getkey(int(key_code))
                logger.info(f"Нажата клавиша: {pressed_key}")
            except:
                logger.warning(f"Неизвестная клавиша")

        for timer in self.data["timers"]:
            if timer["key"] == pressed_key:
                self.start_timer(timer["name"])

    def set_root_window(self, root: tk.Tk):
        """Установка главного окна"""
        self.root = root
        logger.info("Главное окно установлено")

    def start_timer(self, timer_name: str):
        timer_config = next((t for t in self.data["timers"] if t["name"] == timer_name), None)

        if not timer_config:
            logger.error(f"Таймер '{timer_name}' не найден в конфигурации")
            return

        if timer_name in self.active_timers:
            self.stop_timer(timer_name)

        interval = timer_config["interval"]
        end_time = datetime.now() + timedelta(seconds=interval)
        self.timer_end_times[timer_name] = end_time

        def timer_callback():
            logger.info(f"Таймер '{timer_name}' завершен")
            self._show_notification(timer_name)

            # Удаляем из активных таймеров
            self.active_timers.pop(timer_name, None)
            self.timer_end_times.pop(timer_name, None)

            # Обновляем UI
            self._safe_update_ui()

        # Создаем и запускаем таймер
        timer = threading.Timer(interval, timer_callback)
        timer.daemon = True
        timer.start()

        self.active_timers[timer_name] = timer

        logger.info(f"Запущен таймер '{timer_name}' на {interval}сек, завершение в {end_time.strftime('%H:%M:%S')}")
        self._safe_show_status_window()

    def stop_timer(self, timer_name: str):
        if timer_name in self.active_timers:
            self.active_timers[timer_name].cancel()
            self.active_timers.pop(timer_name)
            self.timer_end_times.pop(timer_name, None)
            logger.info(f"Таймер '{timer_name}' остановлен")
            self._safe_update_ui()
        else:
            logger.warning(f"Таймер '{timer_name}' не активен")

    def _show_notification(self, timer_name: str):
        """Показать уведомление о завершении таймера"""
        if self.root:
            self.root.after(0, lambda: self._create_notification_window(timer_name))

    def _create_notification_window(self, timer_name: str):
        """Создание окна уведомления"""
        window = tk.Toplevel(self.root)
        window.title("Таймер завершен")
        window.geometry("300x250")
        window.resizable(False, False)
        window.attributes("-topmost", True)

        # Центрирование
        window.update_idletasks()
        x = (window.winfo_screenwidth() - window.winfo_width()) // 2
        y = (window.winfo_screenheight() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")

        ttk.Label(window, text=f"⏰ Таймер '{timer_name}' завершен!",
                  font=("Arial", 12, "bold")).pack(pady=20)

        ttk.Label(window, text=f"Время: {datetime.now().strftime('%H:%M:%S')}").pack(pady=5)

        ttk.Button(window, text="OK", command=window.destroy, width=10).pack(pady=10)

        window.bell()  # Звуковой сигнал

    def _safe_update_ui(self):
        """Безопасное обновление UI из главного потока"""
        if self.root:
            self.root.after(0, self._update_status_window)

    def _update_status_window(self):
        """Обновление окна статуса"""
        if not self.status_labels:
            return

        current_time = datetime.now()

        for timer_name, label in self.status_labels.items():
            if timer_name in self.timer_end_times:
                remaining = self.timer_end_times[timer_name] - current_time
                if remaining.total_seconds() > 0:
                    mins, secs = divmod(int(remaining.total_seconds()), 60)
                    label.config(text=f"{mins:02d}:{secs:02d}", foreground="green")
                else:
                    label.config(text="завершен", foreground="blue")
            else:
                label.config(text="не активен", foreground="red")

    def _safe_show_status_window(self):
        """Безопасное отображение окна статуса"""
        if self.root:
            self.root.after(0, self._show_status_window)

    def _show_status_window(self):
        """Показать окно статуса"""
        if not self.status_window or not self.status_window.winfo_exists():
            self._create_status_window()

    def _create_status_window(self):
        """Создание окна статуса"""
        if self.status_window and self.status_window.winfo_exists():
            return

        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Статус таймеров")
        self.status_window.geometry("500x400")
        self.status_window.resizable(True, True)
        self.status_window.attributes("-topmost", True)

        # Заголовок
        header = ttk.Label(self.status_window, text="⏰ Активные таймеры",
                           font=("Arial", 14, "bold"))
        header.pack(pady=10)

        # Фрейм для таймеров
        frame = ttk.Frame(self.status_window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.status_labels = {}

        for timer in self.data["timers"]:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill=tk.X, pady=2)

            # Информация о таймере
            info_text = f"{timer['key']} → {timer['name']} ({timer['interval']}сек)"
            info_label = ttk.Label(row_frame, text=info_text, width=40, anchor="w")
            info_label.pack(side=tk.LEFT)

            # Статус
            status_label = ttk.Label(row_frame, text="не активен", width=15)
            status_label.pack(side=tk.RIGHT)

            self.status_labels[timer["name"]] = status_label

        # Кнопка закрытия
        close_btn = ttk.Button(self.status_window, text="Закрыть",
                               command=self._close_status_window)
        close_btn.pack(pady=10)

        # Запуск обновления
        self._start_status_updates()

    def _start_status_updates(self):
        """Запуск периодического обновления статуса"""

        def update():
            if self.status_window and self.status_window.winfo_exists():
                self._update_status_window()
                self.root.after(1000, update)

        if self.root:
            self.root.after(1000, update)

    def _close_status_window(self):
        """Закрытие окна статуса"""
        if self.status_window:
            self.status_window.destroy()
            self.status_window = None

    def stop_all_timers(self):
        """Остановка всех таймеров"""
        for timer_name in list(self.active_timers.keys()):
            self.stop_timer(timer_name)
        logger.info("Все таймеры остановлены")

    def stop(self):
        self.stop_all_timers()
        if self.listener:
            self.listener.stop()
            logger.info("Listener stopped.")

    def start(self):
        logger.info(f"Program ready. Press ctrl_l + esc to stop.")
        with keyboard.Listener(on_press=self.__on_press) as self.listener:
            self.listener.join()


if __name__ == "__main__":
    timer_system = TimerSystem("111.json")
    timer_system.start()