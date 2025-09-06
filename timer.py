import json
import time
import threading
import keyboard
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Any
from GUI.gui_timeout import gui_timeout


class TimerSystem:
    def __init__(self, config_file: str = "timers_config.json"):
        self.config_file = config_file if config_file.endswith(".json") else config_file + ".json"
        self.data = self.load_config()
        self.active_timers: Dict[str, threading.Timer] = {}
        self.timer_end_times: Dict[str, datetime] = {}

        print("Загружена конфигурация таймеров:")
        for timer in self.data.get("timers", []):
            print(f"  {timer['name']}: {timer['interval']}ms, клавиша '{timer['key']}'")

    def load_config(self) -> Dict[str, Any]:
        with open(f"Timers/{self.config_file}", "r") as f:
            return json.load(f)

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
            return

        # Вычисляем время окончания
        end_time = datetime.now() + timedelta(seconds=timer_config["interval"])
        self.timer_end_times[timer_name] = end_time

        def timer_callback():
            # Вызываем callback функцию
            print(f"⏰ ТАЙМЕР '{timer_name}' ЗАВЕРШЕН! Время: {datetime.now().strftime('%H:%M:%S')}")

            gui_timeout(timer_name=timer_name)

            # Удаляем из активных таймеров
            if timer_name in self.active_timers:
                del self.active_timers[timer_name]
            if timer_name in self.timer_end_times:
                del self.timer_end_times[timer_name]

        # Создаем и запускаем таймер
        interval_seconds = timer_config["interval"]
        self.active_timers[timer_name] = threading.Timer(interval_seconds, timer_callback)
        self.active_timers[timer_name].start()

        print(f"▶️ Запущен таймер '{timer_name}' на {interval_seconds / 60:.1f} минут")
        print(f"   Завершится в: {end_time.strftime('%H:%M:%S')}")

    def stop_timer(self, timer_name: str):
        """Останавливает таймер"""
        if timer_name in self.active_timers:
            self.active_timers[timer_name].cancel()
            del self.active_timers[timer_name]
            if timer_name in self.timer_end_times:
                del self.timer_end_times[timer_name]
            print(f"⏹️ Таймер '{timer_name}' остановлен")
        else:
            print(f"Таймер '{timer_name}' не активен")

    def show_status(self):
        """Показывает статус всех таймеров"""
        print("\n" + "=" * 50)
        print("СТАТУС ТАЙМЕРОВ:")
        print("=" * 50)

        if not self.active_timers:
            print("Нет активных таймеров")
            return

        current_time = datetime.now()
        for timer_name, end_time in self.timer_end_times.items():
            remaining = end_time - current_time
            if remaining.total_seconds() > 0:
                mins, secs = divmod(int(remaining.total_seconds()), 60)
                print(f"⏰ {timer_name}: осталось {mins} мин {secs} сек")
            else:
                print(f"⏰ {timer_name}: завершен")

    def setup_keyboard_hotkeys(self):
        """Настраивает горячие клавиши для запуска таймеров"""
        print("\nНастройка горячих клавиш...")

        for timer in self.data.get("timers", []):
            key = timer["key"]
            name = timer["name"]

            # Создаем замыкание для сохранения имени таймера
            def create_callback(timer_name):
                def callback():
                    print(f"\n🎯 Нажата клавиша {key} - запуск таймера '{timer_name}'")
                    self.start_timer(timer_name)
                    self.show_status()

                return callback

            # Регистрируем горячую клавишу
            keyboard.add_hotkey(key, create_callback(name))
            print(f"  {key} → {name}")

    def start(self):
        """Запускает систему таймеров"""
        print("🚀 Система таймеров запущена!")
        print("Нажмите Ctrl+Esc для выхода")


        # Настраиваем горячие клавиши для таймеров
        self.setup_keyboard_hotkeys()

        # Бесконечный цикл ожидания
        try:
            keyboard.wait('ctrl+esc')  # Ожидаем Escape для выхода
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()
        return True


    def stop_all(self):
        """Останавливает все таймеры и выходит"""
        print("\n🛑 Остановка всех таймеров...")
        for timer_name in list(self.active_timers.keys()):
            self.stop_timer(timer_name)