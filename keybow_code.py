# There are two layers, switch by pressing key 3 (top left), 

# The layer colors are as follows:

#  * layer 1: used for pycaw media controls and - = \ that I use for discord mute defen and overlay respectively
#       * green: F13 - F15  Audio controls 1
#       * blue: F18 - F18  Audio controls 2
#       * purple: F19 - F21  Audio controls 3
#       * yellow: F22 - F24  Audio controls 4
#  * layer 2: pink: 0 - 9 keypad inputs and keypad - and x

import board
import time
from keybow2040 import Keybow2040

import usb_hid
from lib.adafruit_hid.keyboard import Keyboard
from lib.adafruit_hid.keycode import Keycode

# Set up Keybow
i2c = board.I2C()
keybow = Keybow2040(i2c)
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)

# keycodes to be picked up by pycaw_listener.py for audio adjustments
# all buttons on this layer are prefixed by alt
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
# 
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

# Define what keys handle each layer
layers =      {1: layer_1,
               2: layer_2}

# Define the layer switch key
next_layer = keys[3]

# Start on layer 1
current_layer = 1

# Define Colors
audio_dial_colors = [(50, 255, 0), #green
                     (0, 130, 255), # blue
                     (130, 0, 255), # purple
                     (138, 255, 38)] # yellow

next_layer_color = (255, 255, 255)

keybind1_color = (255, 255, 0) # yellow
keybind2_color = (255, 120, 0) # orange
keybind3_color = (255, 0, 0) # red


layer_1_colors = {0: audio_dial_colors[0],
                  1: audio_dial_colors[0],
                  2: audio_dial_colors[0],
                  3: next_layer_color,
                  4: audio_dial_colors[1],
                  5: audio_dial_colors[1],
                  6: audio_dial_colors[1],
                  7: keybind1_color,
                  8: audio_dial_colors[2],
                  9: audio_dial_colors[2],
                  10: audio_dial_colors[2],
                  11: keybind2_color,
                  12: audio_dial_colors[3],
                  13: audio_dial_colors[3],
                  14: audio_dial_colors[3],
                  15: keybind3_color}

layer_2_color = (255, 0, 255) # pink

layer_keys = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14]

# Set the LEDs for each key in the current layer
keys[3].set_led(*next_layer_color)
for k in layers[current_layer].keys():
    if current_layer == 1:
        keys[k].set_led(*layer_1_colors[k])
    else:
        keys[k].set_led(*layer_2_color)

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

    # This handles the layer toggle behaviour
    if next_layer.pressed:
        current_layer = current_layer % 2 + 1
        
        # Set the key LEDs first to off, then to their layer colour
        for k in layer_keys:
            keys[k].set_led(0, 0, 0)
            #next_layer.set_led(next_layer_color)

        for k in layers[current_layer].keys():
            if current_layer == 1:
                keys[k].set_led(*layer_1_colors[k])
            else:
                keys[k].set_led(*layer_2_color)


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
                if current_layer == 1:
                    debounce = long_debounce
                    keyboard.send(Keycode.RIGHT_ALT, key_press)
                    
                # Keypad
                elif current_layer == 2:
                    debounce = long_debounce
                    keyboard.send(key_press)
                    

    # If enough time has passed, reset the fired variable
    if fired and time.monotonic() - keybow.time_of_last_press > debounce:
        fired = False