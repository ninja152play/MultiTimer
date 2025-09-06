@echo off
chcp 65001 > nul

echo Проверяю наличие виртуального окружения...
if not exist "venv\" (
    echo Виртуальное окружение не найдено, создаю...
    python -m venv venv
    if errorlevel 1 (
        echo Ошибка при создании venv. Проверьте установлен ли Python
        pause
        exit /b 1
    )
) else (
    echo Виртуальное окружение найдено
)

echo Активирую виртуальное окружение...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Ошибка активации виртуального окружения
    pause
    exit /b 1
)

echo Проверяю наличие requirements.txt...
if exist "requirements.txt" (
    echo Устанавливаю зависимости...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Ошибка установки зависимостей
        pause
        exit /b 1
    )
) else (
    echo Файл requirements.txt не найден, пропускаю установку зависимостей
)

echo Запускаю main.py...
start "" python main.py
