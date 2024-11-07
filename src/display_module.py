# display_module.py

from machine import I2C, Pin
import ssd1306


class Display:
    def __init__(self, scl_pin=5, sda_pin=4, width=128, height=64):
        self.i2c = I2C(scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c)
        self.width = width
        self.height = height

    def clear(self):
        self.display.fill(0)

    def show(self):
        self.display.show()

    def draw_text(self, text, x, y):
        self.display.text(text, x, y)

    def draw_char(self, char, x, y):
        self.display.text(char, x, y)

    def update_display(self, game_map, score):
        self.clear()
        for y in range(len(game_map)):
            for x in range(len(game_map[y])):
                char = game_map[y][x]
                if char != ' ':
                    self.draw_char(char, x * 8, y * 8)
        self.draw_text(f"Score: {score}", 0, len(game_map) * 8)
        self.show()