import time
import keyboard as kb

# ----------------------------
# USB HID Keycode Definitions
# ----------------------------

MODIFIERS = {
    'LeftCtrl': 0x01,
    'LeftShift': 0x02,
    'LeftAlt': 0x04,
    'LeftGUI': 0x08,
    'RightCtrl': 0x10,
    'RightShift': 0x20,
    'RightAlt': 0x40,
    'RightGUI': 0x80
}

MODIFIER_KEYS = {
    'left ctrl': 'LeftCtrl',
    'right ctrl': 'RightCtrl',
    'ctrl': 'LeftCtrl',
    'left shift': 'LeftShift',
    'right shift': 'RightShift',
    'shift': 'LeftShift',
    'left alt': 'LeftAlt',
    'right alt': 'RightAlt',
    'alt': 'LeftAlt',
    'left windows': 'LeftGUI',
    'right windows': 'RightGUI',
    'windows': 'LeftGUI',
    'command': 'LeftGUI',
}

CHARACTER_KEYCODES = {
    **{chr(i): (0x04 + i - ord('a'), False) for i in range(ord('a'), ord('z')+1)},
    **{chr(i).upper(): (0x04 + i - ord('a'), True) for i in range(ord('a'), ord('z')+1)},
    '1': (0x1E, False), '!': (0x1E, True),
    '2': (0x1F, False), '@': (0x1F, True),
    '3': (0x20, False), '#': (0x20, True),
    '4': (0x21, False), '$': (0x21, True),
    '5': (0x22, False), '%': (0x22, True),
    '6': (0x23, False), '^': (0x23, True),
    '7': (0x24, False), '&': (0x24, True),
    '8': (0x25, False), '*': (0x25, True),
    '9': (0x26, False), '(': (0x26, True),
    '0': (0x27, False), ')': (0x27, True),
    ' ': (0x2C, False),
    '-': (0x2D, False), '_': (0x2D, True),
    '=': (0x2E, False), '+': (0x2E, True),
    '[': (0x2F, False), '{': (0x2F, True),
    ']': (0x30, False), '}': (0x30, True),
    '\\': (0x31, False), '|': (0x31, True),
    ';': (0x33, False), ':': (0x33, True),
    '\'': (0x34, False), '"': (0x34, True),
    '`': (0x35, False), '~': (0x35, True),
    ',': (0x36, False), '<': (0x36, True),
    '.': (0x37, False), '>': (0x37, True),
    '/': (0x38, False), '?': (0x38, True),
    '\n': (0x28, False), 'enter': (0x28, False),
    '\t': (0x2B, False), 'tab': (0x2B, False),
    'backspace': (0x2A, False),
    'esc': (0x29, False), 'escape': (0x29, False),
    'delete': (0x4C, False),
    'insert': (0x49, False),
    'home': (0x4A, False),
    'end': (0x4D, False),
    'page up': (0x4B, False),
    'page down': (0x4E, False),
    'arrow up': (0x52, False), 'up': (0x52, False),
    'arrow down': (0x51, False), 'down': (0x51, False),
    'arrow left': (0x50, False), 'left': (0x50, False),
    'arrow right': (0x4F, False), 'right': (0x4F, False),
    'caps lock': (0x39, False),
    'pause': (0x48, False), 'break': (0x48, False), 'pause/break': (0x48, False),
}

for i in range(1, 13):
    CHARACTER_KEYCODES[f'f{i}'] = (0x3A + (i - 1), False)
    CHARACTER_KEYCODES[f'F{i}'] = (0x3A + (i - 1), False)

NUMPAD = {
    'numpad 0': (0x62, False), 'numpad 1': (0x59, False), 'numpad 2': (0x5A, False), 'numpad 3': (0x5B, False),
    'numpad 4': (0x5C, False), 'numpad 5': (0x5D, False), 'numpad 6': (0x5E, False), 'numpad 7': (0x5F, False),
    'numpad 8': (0x60, False), 'numpad 9': (0x61, False),
    'numpad .': (0x63, False), 'numpad enter': (0x58, False),
    'numpad +': (0x57, False), 'numpad -': (0x56, False),
    'numpad *': (0x55, False), 'numpad /': (0x54, False),
}
CHARACTER_KEYCODES.update(NUMPAD)

SPECIAL_KEY_ALIASES = {
    'cancel': 'pause',
    'pause/break': 'pause',
    'return': 'enter',
    'del': 'delete',
    'ins': 'insert',
    'pgup': 'page up',
    'pgdn': 'page down',
}

# ----------------------------
# HID Keyboard Sender
# ----------------------------

class HIDKeyboard:
    def __init__(self, device_path='/dev/hidg0'):
        self.device_path = device_path

    def write_report(self, report):
        with open(self.device_path, 'rb+') as fd:
            fd.write(report)

    def press_key(self, keycode, modifiers=0):
        report = bytearray(8)
        report[0] = modifiers
        report[2] = keycode
        self.write_report(report)

    def release_keys(self):
        self.write_report(bytearray(8))

    def press_character(self, char, extra_modifiers=[]):
        char = SPECIAL_KEY_ALIASES.get(char, char)
        if char not in CHARACTER_KEYCODES:
            print(f"[!] Unsupported character: {repr(char)}")
            return

        keycode, needs_shift = CHARACTER_KEYCODES[char]
        modifier_byte = 0

        if needs_shift:
            modifier_byte |= MODIFIERS['LeftShift']
        for mod in extra_modifiers:
            modifier_byte |= MODIFIERS.get(mod, 0)

        self.press_key(keycode, modifier_byte)
        time.sleep(0.05)
        self.release_keys()

    def press_modifier(self, mod_name):
        if mod_name not in MODIFIERS:
            print(f"[!] Unsupported modifier: {mod_name}")
            return
        report = bytearray(8)
        report[0] = MODIFIERS[mod_name]
        self.write_report(report)
        time.sleep(0.05)
        self.release_keys()

# ----------------------------
# Real-Time Key Processing
# ----------------------------

keyboard = HIDKeyboard()
pressed_modifiers = set()
caps_lock_active = False

def on_press(event):
    global caps_lock_active

    key = event.name.lower()
    print(key)

    # Handle Caps Lock toggle
    if key == 'caps lock':
        caps_lock_active = not caps_lock_active
        print(f"[Caps Lock] {'ON' if caps_lock_active else 'OFF'}")
        return

    # Handle modifier keys: Shift and Alt are added on press
    if key in MODIFIER_KEYS:
        mod = MODIFIER_KEYS[key]
        pressed_modifiers.add(mod)
        keyboard.press_modifier(mod)
        return

    # Map aliases and whitespace
    char = SPECIAL_KEY_ALIASES.get(key, key)
    if key == 'space':
        char = ' '
    elif key == 'enter':
        char = '\n'
    elif key == 'tab':
        char = '\t'
    elif key == 'backspace':
        char = 'backspace'
    elif key == 'esc':
        char = 'esc'
    elif key in NUMPAD:
        char = key
    elif len(key) == 1:
        # Letter or symbol
        if key.isalpha():
            shift_active = 'LeftShift' in pressed_modifiers or 'RightShift' in pressed_modifiers
            if caps_lock_active ^ shift_active:
                char = key.upper()
            else:
                char = key.lower()
        else:
            shift_active = 'LeftShift' in pressed_modifiers or 'RightShift' in pressed_modifiers
            if shift_active:
                for ch, (code, shifted) in CHARACTER_KEYCODES.items():
                    base_code = CHARACTER_KEYCODES.get(key, (None, None))[0]
                    if shifted and base_code == code:
                        char = ch
                        break
                else:
                    char = key
            else:
                char = key

    print(f"Sending: {repr(char)} (CapsLock: {caps_lock_active}, Modifiers: {pressed_modifiers})")

    with open('logs.txt', 'a') as f:
        f.write(f"{repr(char)}\n")

    keyboard.press_character(char, list(pressed_modifiers))
    if "LeftShift" in pressed_modifiers:
        pressed_modifiers.remove("LeftShift")
    elif "RightShift" in pressed_modifiers:
        pressed_modifiers.remove("RightShift")
    elif "LeftCtrl" in pressed_modifiers: 
        pressed_modifiers.remove("LeftCtrl")
    elif "RightCtrl" in pressed_modifiers:
        pressed_modifiers.remove("RightCtrl")
    elif "LeftAlt" in pressed_modifiers:
        pressed_modifiers.remove("LeftAlt")
    elif "RightAlt" in pressed_modifiers:
        pressed_modifiers.remove("RightAlt")

def on_release(event):
    key = event.name.lower()
    if key in MODIFIER_KEYS:
        mod = MODIFIER_KEYS[key]
        if mod in pressed_modifiers:
            pressed_modifiers.discard(mod)
            keyboard.release_keys()

print("🔴 Live USB HID Keyboard Emulation Started.")
kb.on_press(on_press)
kb.on_release(on_release)

import signal

def handler(signum, frame):
    print("Ctrl+C ignored.")

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTSTP, handler) 
try:
    while True:
        time.sleep(1)
except Exception as e:
    print(f"Errore: {e}")
