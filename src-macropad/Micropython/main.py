import board
import busio
import time
import usb_hid
import digitalio
import adafruit_ssd1306
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Button mapping
BTN1_PIN = board.GP6
BTN2_PIN = board.GP8
BTN3_PIN = board.GP11
BTN4_PIN = board.GP7
BTN5_PIN = board.GP10
BTN6_PIN = board.GP12

buttons = [
    digitalio.DigitalInOut(BTN1_PIN),
    digitalio.DigitalInOut(BTN2_PIN),
    digitalio.DigitalInOut(BTN3_PIN),
    digitalio.DigitalInOut(BTN4_PIN),
    digitalio.DigitalInOut(BTN5_PIN),
    digitalio.DigitalInOut(BTN6_PIN),
]

for btn in buttons:
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN

NUM_BUTTONS = len(buttons)

# OLED display setup
WIDTH = 128
HEIGHT = 32

# I2C pins
SCL = 5
SDA = 4

BTN_DOWN = 1
BTN_UP = 0

lastState = BTN_UP

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

modes = [
    {
        "name": "Teams",
        "functions": [
            {
                "name": "Search",
                "func": lambda: keyboard.send(Keycode.LEFT_CONTROL, Keycode.E),
            },
            {
                "name": "Goto",
                "func": lambda: keyboard.send(Keycode.LEFT_CONTROL, Keycode.G),
            },
            {
                "name": "Toggle mute",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.M
                ),
            },
            {
                "name": "Toggle camera",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.O
                ),
            },
            {
                "name": "Hangup",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.B
                ),
            },
        ],
    },
    {
        "name": "VS Code",
        "functions": [
            {
                "name": "Explorer",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.E
                ),
            },
            {
                "name": "Problems",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.M
                ),
            },
            {
                "name": "Search",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.F
                ),
            },
            {
                "name": "Debug",
                "func": lambda: keyboard.send(Keycode.F5),
            },
            {
                "name": "Output",
                "func": lambda: keyboard.send(
                    Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.U
                ),
            },
        ],
    },
    {
        "name": "Git",
        "functions": [
            {
                "name": "Branch..",
                "func": lambda: layout.write("git checkout -b "),
            },
            {
                "name": "Checkout main",
                "func": lambda: layout.write("git checkout main\n"),
            },
            {
                "name": "Status",
                "func": lambda: layout.write("git status\n"),
            },
            {
                "name": "Push",
                "func": lambda: layout.write("git push\n"),
            },
            {
                "name": "Pull org main",
                "func": lambda: layout.write("git pull origin main\n"),
            },
        ],
    },
]

currentMode = 0
COUNT_OF_MODES = len(modes)

# Initialize I2C
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)


def handle_mode_press(mode, key):
    if mode < 0 or mode >= COUNT_OF_MODES:
        return

    mode_data = modes[mode]
    if key < 1 or key > len(mode_data["functions"]):
        return

    func_index = key - 1

    func = mode_data["functions"][func_index]["func"]
    func()


def draw_screen(text, x, y):
    display.fill(0)
    display.text(text, x, y, 1)
    display.text("Mode: " + modes[currentMode]["name"], 24, 12, 1)
    display.text("Pikku v1.0", 24, 24, 1)
    display.show()


def buttonPress(last):
    global currentMode
    tempLast = last
    text = ""
    nextState = last

    # Check key 1 mode change
    if (tempLast == BTN_UP) and (buttons[0].value):
        nextState = BTN_DOWN
        currentMode += 1
        if currentMode > COUNT_OF_MODES - 1:
            currentMode = 0

        draw_screen("", 1, 1)

    # Check keys 1 -> (num buttons - 1) press
    for btn in range(1, NUM_BUTTONS):
        if (tempLast == BTN_UP) and (buttons[btn].value):
            nextState = BTN_DOWN
            text = modes[currentMode]["functions"][btn - 1]["name"]
            draw_screen(text, 1, 1)
            # Type the text as key presses
            handle_mode_press(currentMode, btn)
            time.sleep(0.256)

    any_button_pressed = any(buttons[i].value for i in range(NUM_BUTTONS))

    # Key up
    if tempLast == BTN_DOWN and not any_button_pressed:
        nextState = BTN_UP
        draw_screen("", 1, 1)

    return nextState


draw_screen("", 1, 1)
while True:
    lastState = buttonPress(lastState)
