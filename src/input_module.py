# input_module.py

from machine import Pin
import time


class Input:
    def __init__(self, pin_left=14, pin_right=12, pin_up=0, pin_down=13):
        self.buttons = {
            'left': Pin(pin_left, Pin.IN, Pin.PULL_UP),
            'right': Pin(pin_right, Pin.IN, Pin.PULL_UP),
            'up': Pin(pin_up, Pin.IN, Pin.PULL_UP),
            'down': Pin(pin_down, Pin.IN, Pin.PULL_UP),
        }
        self.last_press = {
            'left': 0,
            'right': 0,
            'up': 0,
            'down': 0,
        }
        self.debounce_time = 200  # milliseconds

    def get_pressed(self):
        current_time = time.ticks_ms()
        pressed = []
        for direction, pin in self.buttons.items():
            if not pin.value():
                if time.ticks_diff(current_time, self.last_press[direction]) > self.debounce_time:
                    pressed.append(direction)
                    self.last_press[direction] = current_time
        return pressed