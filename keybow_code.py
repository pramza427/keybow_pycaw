# There are three layers, selected by pressing and holding key 3 (top left), 
# then tapping one of the colored layer selector keys to the right of it

# The layer colors are as follows:

#  * layer 1: used for pycaw media controls and - = \ that I use for discord mute defen and overlay respectively
#       * pink: F13 - F15  Audio controls 1
#       * blue: F18 - F18  Audio controls 2
#       * purple: F19 - F21  Audio controls 3
#       * yellow: F22 - F24  Audio controls 4
#  * layer 2: blue: 0 - 9 keypad inputs and keypad - and x : used for quickbuys in games
#  * layer 3: yellow: sends strings on each key press

import board
import time
from keybow2040 import Keybow2040

import usb_hid
from lib.adafruit_hid.keyboard import Keyboard
from lib.adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from lib.adafruit_hid.keycode import Keycode

from lib.adafruit_hid.consumer_control import ConsumerControl
from lib.adafruit_hid.consumer_control_code import ConsumerControlCode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Set up consumer control (used to send media key presses)
consumer_control = ConsumerControl(usb_hid.devices)

# keycodes to be picked up by pycaw_listener.py for audio adjustments
# all buttons on this layer are prefixed by alt
#       (L1) (L2) (L3)
# Layer  -    =    \
#  F15  F18  F21  F24
#  F14  F17  F20  F23
#  F13  F16  F19  F22
#
# Function keys over 20 should have a keycode but break my keybow so I replaced them with their ASCI values
layer_1 =     {0: Keycode.F13,
               1: Keycode.F14,
               2: Keycode.F15,
               4: Keycode.F16,
               5: Keycode.F17,
               6: Keycode.F18,
               7: Keycode.MINUS,
               8: Keycode.F19,
               9: 111, #F20
               10: 112, #F21
               11: Keycode.EQUALS,
               12: 113, #F22
               13: 114, #F23
               14: 115, #F24
               15: Keycode.BACKSLASH
               }

# Layer with keypad 0-9, -, x 
# Mainly used for quick buying in csgo
#   (L1)(L2)(L3)
# L   -   =   \
# 7   8   9   X
# 4   5   6   -
# 1   2   3   0
layer_2 =     {0: Keycode.KEYPAD_ONE,
               4: Keycode.KEYPAD_TWO,
               8: Keycode.KEYPAD_THREE,
               12: Keycode.KEYPAD_ZERO,
               1: Keycode.KEYPAD_FOUR,
               5: Keycode.KEYPAD_FIVE,
               9: Keycode.KEYPAD_SIX,
               13: Keycode.KEYPAD_MINUS,
               2: Keycode.KEYPAD_SEVEN,
               6: Keycode.KEYPAD_EIGHT,
               10: Keycode.KEYPAD_NINE,
               14: Keycode.KEYPAD_ASTERISK,
               7: Keycode.MINUS,
               11: Keycode.EQUALS,
               15: Keycode.BACKSLASH
               }


layer_3 =     {0: "pack ",
               4: "my ",
               8: "box ",
               6: "with ",
               10: "five ",
               14: "dozen ",
               5: "liquor ",
               9: "jugs "}

# Define what keys handle each layer
layers =      {7: layer_1,
               11: layer_2,
               15: layer_3}

# Define the modifier key and layer selector keys
modifier = keys[3]

selectors =   {7: keys[7],
               11: keys[11],
               15: keys[15]}

# Start on layer 1
current_layer = 7

audio_dial_colors = [(255, 89, 94),
                     (25, 130, 255),
                     (106, 76, 255),
                     (138, 255, 38)]

layer_7_colors = {0: audio_dial_colors[0],
                  1: audio_dial_colors[0],
                  2: audio_dial_colors[0],
                  3: audio_dial_colors[0],
                  4: audio_dial_colors[1],
                  5: audio_dial_colors[1],
                  6: audio_dial_colors[1],
                  7: audio_dial_colors[1],
                  8: audio_dial_colors[2],
                  9: audio_dial_colors[2],
                  10: audio_dial_colors[2],
                  11: audio_dial_colors[2],
                  12: audio_dial_colors[3],
                  13: audio_dial_colors[3],
                  14: audio_dial_colors[3],
                  15: audio_dial_colors[3]}

# The colors for each layer
colors = {7: (255, 0, 255),
          11: (0, 255, 255),
          15: (255, 255, 0)}

layer_keys = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14]

# Set the LEDs for each key in the current layer
for k in layers[current_layer].keys():
    if current_layer == 7:
        keys[k].set_led(*layer_7_colors[k])
    else:
        keys[k].set_led(*colors[current_layer])

# To prevent the strings (as opposed to single key presses) that are sent from 
# refiring on a single key press, the debounce time for the strings has to be 
# longer.
short_debounce = 0.03
long_debounce = 0.2
debounce = 0.03
fired = False

while True:
    # Always remember to call keybow.update()!
    keybow.update()

    # This handles the modifier and layer selector behaviour
    if modifier.held:
        # Give some visual feedback for the modifier key
        modifier.led_off()

        # If the modifier key is held, light up the layer selector keys
        for layer in layers.keys():
            keys[layer].set_led(*colors[layer])

            # Change layer if layer key is pressed
            if current_layer != layer:
                if selectors[layer].pressed:
                    current_layer = layer

                    # Set the key LEDs first to off, then to their layer colour
                    for k in layer_keys:
                        keys[k].set_led(0, 0, 0)

                    for k in layers[layer].keys():
                        if current_layer == 7:
                            keys[k].set_led(*layer_7_colors[k])
                        else:
                            keys[k].set_led(*colors[layer])

    # Turn off the layer selector LEDs if the modifier isn't held
    else:
        for layer in layers.keys():
            keys[layer].led_off()

        # Give some visual feedback for the modifier key
        modifier.set_led(0, 255, 25)

    # Loop through all of the keys in the layer and if they're pressed, get the
    # key code from the layer's key map
    for k in layers[current_layer].keys():
        if keys[k].pressed:
            key_press = layers[current_layer][k]

            # If the key hasn't just fired (prevents refiring)
            if not fired:
                fired = True

                # Send the right sort of key press and set debounce for each
                # layer accordingly (layer 2 needs a long debounce)
                # Volume Controls
                if current_layer == 7:
                    debounce = long_debounce
                    keyboard.send(Keycode.RIGHT_ALT, key_press)
                    
                # Keypad
                elif current_layer == 11:
                    debounce = long_debounce
                    keyboard.send(key_press)
                    
                # Strings
                elif current_layer == 15:
                    debounce = short_debounce
                    layout.write(key_press)

    # If enough time has passed, reset the fired variable
    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False