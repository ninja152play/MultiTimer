KEYBOARD_KEYS = {
    # Буквы
    65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f', 71: 'g', 72: 'h',
    73: 'i', 74: 'j', 75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o', 80: 'p',
    81: 'q', 82: 'r', 83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x',
    89: 'y', 90: 'z',

    # Цифры верхнего ряда
    48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7',
    56: '8', 57: '9',

    # Функциональные клавиши
    112: 'f1', 113: 'f2', 114: 'f3', 115: 'f4', 116: 'f5', 117: 'f6',
    118: 'f7', 119: 'f8', 120: 'f9', 121: 'f10', 122: 'f11', 123: 'f12',

    # Цифровая клавиатура (numpad)
    96: 'num 0', 97: 'num 1', 98: 'num 2', 99: 'num 3', 100: 'num 4',
    101: 'num 5', 102: 'num 6', 103: 'num 7', 104: 'num 8', 105: 'num 9',
    107: 'num +', 109: 'num -', 106: 'num *', 111: 'num /', 110: 'num .',

    # Специальные клавиши
    32: 'space', 13: 'enter', 27: 'esc', 9: 'tab', 8: 'backspace',
    20: 'caps lock', 16: 'shift', 17: 'ctrl', 18: 'alt',
    144: 'num lock', 145: 'scroll lock',

    # Стрелки
    37: 'left', 38: 'up', 39: 'right', 40: 'down',

    # Дополнительные клавиши
    192: '`', 189: '-', 187: '=', 219: '[', 221: ']', 186: ';', 222: "'",
    188: ',', 190: '.', 191: '/', 220: '\\',

    # Клавиши с разными названиями для модуля keyboard
    # Добавляем альтернативные названия
    # 38: 'up',  # Стрелка вверх
    # 104: 'numpad 8',  # Num 8 (альтернативное название)
    # 97: 'numpad 1',  # Num 1 (альтернативное название)
}

# Дополнительная таблица для преобразования keysym в названия keyboard
KEYSYM_TO_KEYBOARD = {
    'Up': 'up',
    'Down': 'down',
    'Left': 'left',
    'Right': 'right',
    'Prior': 'page up',
    'Next': 'page down',
    'Home': 'home',
    'End': 'end',
    'Insert': 'insert',
    'Delete': 'delete',
    'Return': 'enter',
    'Escape': 'esc',
    'Tab': 'tab',
    'BackSpace': 'backspace',
    'Caps_Lock': 'caps lock',
    'Shift_L': 'shift',
    'Shift_R': 'shift',
    'Control_L': 'ctrl',
    'Control_R': 'ctrl',
    'Alt_L': 'alt',
    'Alt_R': 'alt',
    'Num_Lock': 'num lock',
    'Scroll_Lock': 'scroll lock',
    'space': 'space',
    'comma': ',',
    'period': '.',
    'slash': '/',
    'semicolon': ';',
    'apostrophe': "'",
    'bracketleft': '[',
    'bracketright': ']',
    'backslash': '\\',
    'grave': '`',
    'minus': '-',
    'equal': '=',
}


def getkey(code, keysym=None):
    """Получает название клавиши для модуля keyboard"""
    # Сначала пробуем получить по keysym (более надежно для специальных клавиш)
    print("code: ", code)
    if keysym and keysym in KEYSYM_TO_KEYBOARD:
        return KEYSYM_TO_KEYBOARD[keysym]

    # Затем по коду
    if code in KEYBOARD_KEYS:
        return KEYBOARD_KEYS[code]

    # Если не нашли, возвращаем None
    return None
