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
    'left shift': 'LeftShift',
    'right shift': 'RightShift',
    'left alt': 'LeftAlt',
    'right alt': 'RightAlt',
    'left windows': 'LeftGUI',
    'right windows': 'RightGUI',
}

CHARACTER_KEYCODES = {
    'a': (0x04, False), 'A': (0x04, True),
    'b': (0x05, False), 'B': (0x05, True),
    'c': (0x06, False), 'C': (0x06, True),
    'd': (0x07, False), 'D': (0x07, True),
    'e': (0x08, False), 'E': (0x08, True),
    'f': (0x09, False), 'F': (0x09, True),
    'g': (0x0A, False), 'G': (0x0A, True),
    'h': (0x0B, False), 'H': (0x0B, True),
    'i': (0x0C, False), 'I': (0x0C, True),
    'j': (0x0D, False), 'J': (0x0D, True),
    'k': (0x0E, False), 'K': (0x0E, True),
    'l': (0x0F, False), 'L': (0x0F, True),
    'm': (0x10, False), 'M': (0x10, True),
    'n': (0x11, False), 'N': (0x11, True),
    'o': (0x12, False), 'O': (0x12, True),
    'p': (0x13, False), 'P': (0x13, True),
    'q': (0x14, False), 'Q': (0x14, True),
    'r': (0x15, False), 'R': (0x15, True),
    's': (0x16, False), 'S': (0x16, True),
    't': (0x17, False), 'T': (0x17, True),
    'u': (0x18, False), 'U': (0x18, True),
    'v': (0x19, False), 'V': (0x19, True),
    'w': (0x1A, False), 'W': (0x1A, True),
    'x': (0x1B, False), 'X': (0x1B, True),
    'y': (0x1C, False), 'Y': (0x1C, True),
    'z': (0x1D, False), 'Z': (0x1D, True),

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

    '\n': (0x28, False),  # Enter
    '\t': (0x2B, False),  # Tab
    'backspace': (0x2A, False),
    'esc': (0x29, False)
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
        report[0] = modifiers      # Modifier byte
        report[2] = keycode        # Keycode (first key)
        self.write_report(report)

    def release_keys(self):
        self.write_report(bytearray(8))  # Send 0s to release

    def press_character(self, char, extra_modifiers=[]):
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

# ----------------------------
# Real-Time Key Processing
# ----------------------------

keyboard = HIDKeyboard()
pressed_modifiers = set()

# Manual state
shift_active_once = False
caps_lock_active = False

def on_press(event):
    global shift_active_once, caps_lock_active

    key = event.name.lower()
    with open('logs.txt', 'a') as f:
        f.write(f"{key}\n")
    print(key)
    # Handle modifier keys
    if key == 'shift':
        shift_active_once = True
    if key == 'caps lock':
        caps_lock_active = not caps_lock_active
        print(f"[Caps Lock] {'ON' if caps_lock_active else 'OFF'}")
        return

    # Special keys
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
    elif len(key) == 1:
        # Apply caps lock or shift
        if key.isalpha():
            if caps_lock_active or shift_active_once:
                char = key.upper()
            else:
                char = key.lower()
        else:
            # For symbols, try to get the shifted version if shift is active
            if shift_active_once:
                for ch, (code, shifted) in CHARACTER_KEYCODES.items():
                    base_code = CHARACTER_KEYCODES.get(key, (None, None))[0]
                    if shifted and base_code == code:
                        char = ch
                        break
                else:
                    char = key
            else:
                char = key
    else:
        return

    print(f"Sending: {repr(char)} (ShiftOnce: {shift_active_once}, CapsLock: {caps_lock_active})")
    keyboard.press_character(char)

    # Clear one-time shift
    shift_active_once = False

def on_release(event):
    key = event.name.lower()
    if key in MODIFIER_KEYS:
        mod = MODIFIER_KEYS[key]
        pressed_modifiers.discard(mod)

# ----------------------------
# Start Real-Time Listening
# ----------------------------

print("🔴 Live USB HID Keyboard Emulation Started. Waiting for the time running out.")
kb.on_press(on_press)
kb.on_release(on_release)

# Block until the time runs out is pressed
time.sleep(999999)
print("🛑 Stopped.")
