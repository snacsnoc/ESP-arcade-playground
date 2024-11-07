# Game Hub for ESP8266/ESP32 🎮🚀

A small game framework for the ESP8266 using MicroPython, featuring multiple games that run on an SSD1306 OLED display. Easily manage and switch between multiple games from the menu. 
## Features

- Simplified structure to add and manage multiple games.
- Includes:
  - Dodge game: dodge the falling Os
  - Collect Stars: run around and collect stars (
  - Zombie game: reach the exit before the zombies catch you
- Requires only 4 button controls for navigation and game controls.
- Uses an inexpensive OLED display

## Hardware Requirements

- **ESP8266 or ESP32**
- **SSD1306 OLED Display**: 128x64 pixels (SCL pin: 5, SDA pin: 4)
- **Buttons**: For navigation and game controls (minimum 2-4 buttons, configured as follows):
  * Left Button: GPIO 14
  * Right Button: GPIO 12
  * Up Button: GPIO 0
  * Down Button: GPIO 13

## Personal Requirements

- **Smile on your face**

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/snacsnoc/ESP-arcade-playground.git
   cd ESP-arcade-playground
   ```

2. **Upload files to ESP8266:**
   Make sure your ESP8266 is connected
   In the mpfshell prompt, run:
    ```bash
    mpfshell -n -c "open tty.usbserial-0001; lcd src; mput .*\.py; md games; lcd games; cd games; mput .*\.py"    
    ```

   Replace `tty.usbserial-0001` with your ESP8266's serial port.


3. **Set up firmware:**
   Flash the latest MicroPython firmware on your ESP8266 if not already done, v1.23 and 1.24 have been tested.

## Usage


* Connect the GPIOs appropriately as above, plug the ESP8266 in to power. The device will boot and display the main menu on the OLED screen.
* Use the connected buttons to navigate between different games.
* Select a game with the right button and use the buttons to control the player and play games.
* Tell all your friends about it and have fun!


## Game Development
### Steps to add a new game

1. **Create a new game file**:
   - Create a new Python file for your game in the `src/games/` directory.
   - Name your file with a descriptive name, using snake_case (e.g., `new_game.py`).

2. **Game Class Definition**:
   - Your game should define a class that inherits from the `Game` class in `game_framework.py`.
   - Implement the necessary methods such as `initialize_game()`, `run()`, and any other methods required for your game logic.

   Example structure:
   ```python
   from game_framework import Game

   class NewGame(Game):
       def initialize_game(self):
           # Initialize game variables, set up the game environment
           pass

       def run(self):
           # Main game loop
           pass

3. Integrating with Game Manager:
* If you want your game to be selectable from the main menu, add an entry in `game_manager.py` for your new game. 
* See the existing format in `game_manager.py` for examples.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE-MIT) file for details.

