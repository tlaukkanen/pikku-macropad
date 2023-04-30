import board
import digitalio
import rotaryio
import time
import usb_hid
import adafruit_hid.keyboard as keyboard
import adafruit_hid.mouse as mouse
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Define pins
DT_PIN = board.GP19
CLK_PIN = board.GP18
SW_PIN = board.GP20

BTN_DOWN = 1
BTN_UP = 0

button = digitalio.DigitalInOut(SW_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN
last_button_state = BTN_UP
last_position = None

# Define initial mode
mode = "VOL"

# Define keyboard layout
pikku_keyboard = keyboard.Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(pikku_keyboard)
cc = ConsumerControl(usb_hid.devices)
pikku_mouse = mouse.Mouse(usb_hid.devices)

# Define rotary encoder callback function
def change_mode():
    global mode
    if mode == "VOL":
        mode = "SCROLL"
    elif mode == "SCROLL":
        mode = "CURSOR"
    elif mode == "CURSOR":
        mode = "FIDGET"
    else:
        mode = "VOL"
    time.sleep(0.1)

# Define rotary encoder reading function
def read_encoder(encoder):
    global last_position
    position = encoder.position
    if last_position == None or position == last_position:
        last_position = position
        return 0
    delta = last_position - position
    last_position = position
    return delta

# Create rotary encoder object
encoder = rotaryio.IncrementalEncoder(DT_PIN, CLK_PIN)

# Define main loop
while True:
    # Read rotary encoder
    encoder_delta = read_encoder(encoder)
    if encoder_delta != 0:
        print("delta: " + str(encoder_delta))

    # Adjust volume, scroll or cursor based on mode
    if mode == "VOL":
        if encoder_delta > 0:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        elif encoder_delta < 0:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    elif mode == "SCROLL":
        if encoder_delta > 0:
            pikku_mouse.move(wheel=-1)
        elif encoder_delta < 0:
            pikku_mouse.move(wheel=1)
    elif mode == "CURSOR":
        if encoder_delta > 0:
            pikku_keyboard.send(Keycode.DOWN_ARROW)
        elif encoder_delta < 0:
            pikku_keyboard.send(Keycode.UP_ARROW)
    else:
        # Fidget mode - do nothing
        if encoder_delta > 0:
            print("right")
        elif encoder_delta < 0:
            print("left")

    # Check if rotary encoder switch is pressed
    if button.value is False and last_button_state == BTN_UP:
        change_mode()
        print("new mode: " + mode) 
        last_button_state = BTN_DOWN
        time.sleep(0.1)
    else:
        last_button_state = BTN_UP

    # Delay to avoid debounce
    time.sleep(0.02)
