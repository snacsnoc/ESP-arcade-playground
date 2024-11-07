# game_manager.py

from display_module import Display
from input_module import Input
import time
from games.zombie_game import ZombieGame
from games.collect_stars import CollectStars
from games.dodge_game import DodgeGame


class GameManager:
    def __init__(self):
        """
        Initialize the Game Manager with display and input modules.
        """
        self.display = Display()
        self.input = Input()
        self.current_game = None
        self.games = [
            {
                "name": "Zombie Game",
                "class": ZombieGame,
                "params": {
                    "map_width": 16,
                    "map_height": 8,
                    "num_zombies": 3,
                    "num_walls": 5,
                    "zombie_move_period": 2000,
                },
            },
            {
                "name": "Collect Stars",
                "class": CollectStars,
                "params": {
                    "map_width": 16,
                    "map_height": 8,
                    "num_zombies": 2,
                    "num_walls": 5,
                    "num_stars": 5,
                    "zombie_move_period": 1000,
                },
            },
            {
                "name": "Dodge Objects",
                "class": DodgeGame,
                "params": {
                    "map_width": 16,
                    "map_height": 8,
                    "num_walls": 2,
                    "object_spawn_interval": 2,
                    "object_fall_speed": 1,
                },
            },
        ]
        self.selected_index = 0

    def display_menu(self):
        """
        Display the main menu allowing the player to select a game
        """
        self.display.clear()
        self.display.draw_text("Select Game:", 20, 3)
        for idx, game in enumerate(self.games):
            y_position = 20 + (idx + 1) * 10
            if idx == self.selected_index:
                self.display.draw_text("-> " + game["name"], 5, y_position)
            else:
                self.display.draw_text("   " + game["name"], 5, y_position)
        self.display.show()

    def get_menu_selection(self):
        """
        Wait for the user to navigate the menu using Up/Down buttons
        and select a game using the Right button.

        :return: None
        """
        while True:
            pressed = self.input.get_pressed()
            if "up" in pressed:
                self.selected_index = (self.selected_index - 1) % len(self.games)
                self.display_menu()
                # Debounce delay
                time.sleep(0.3)
            elif "down" in pressed:
                self.selected_index = (self.selected_index + 1) % len(self.games)
                self.display_menu()
                time.sleep(0.3)
            elif "right" in pressed:
                selected_game = self.games[self.selected_index]
                if selected_game["class"] is not None:
                    self.launch_game(selected_game["class"], selected_game["params"])
                break
            # Small delay to prevent CPU hogging
            time.sleep(0.05)

    def launch_game(self, game_class, game_params):
        """
        Instantiate and run the selected game

        :param game_class: The class of the game to be launched.
        :param game_params: A dictionary of parameters specific to the game.
        """
        try:
            # Instantiate the game with its specific parameters using ** unpacking
            game_instance = game_class(**game_params)
            # Run the game (this will take over until the game ends and resets the device)
            game_instance.run()
        except TypeError as e:
            # Handle cases where incorrect parameters are passed
            self.display.clear()
            self.display.draw_text("Error Launching", 25, 20)
            self.display.draw_text(str(e), 0, 30)
            self.display.show()
            time.sleep(3)
            self.display_menu()

    def run(self):
        """
        Display the menu, get user selection, and launch the selected game
        """
        self.display_menu()
        self.get_menu_selection()
