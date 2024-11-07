# game_framework.py

import time
from machine import Timer
from display_module import Display
from input_module import Input


class Game:
    def __init__(self, map_width=16, map_height=8, update_period=1000):
        """
        Initialize the game framework.

        :param map_width: Width of the game map in cells.
        :param map_height: Height of the game map in cells.
        :param update_period: Period (in milliseconds) for periodic updates (e.g., moving zombies).
        """
        self.display = Display()
        self.input = Input()
        self.map_width = map_width
        self.map_height = map_height
        self.update_period = update_period
        self.game_map = []
        self.score = 0
        self.game_over_flag = False
        self.game_win_flag = False
        self.timer = Timer(-1)

    def initialize_game(self):
        """
        Initialize game state.
        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "initialize_game() must be implemented by the subclass."
        )

    def handle_input(self, direction):
        """
        Handle user input.
        Must be implemented by subclasses.

        :param direction: Direction input by the user (e.g., 'left', 'right', 'up', 'down').
        """
        raise NotImplementedError("handle_input() must be implemented by the subclass.")

    def update_state(self, timer):
        """
        Update game state periodically.
        Must be implemented by subclasses.

        :param timer: Timer object triggering the update.
        """
        raise NotImplementedError("update_state() must be implemented by the subclass.")

    def render(self):
        """
        Render the current game state to the display.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("render() must be implemented by the subclass.")

    def game_over_screen(self):
        """
        Display the game over screen.
        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "game_over_screen() must be implemented by the subclass."
        )

    def game_win_screen(self):
        """
        Display the game win screen.
        Must be implemented by subclasses.
        """
        raise NotImplementedError(
            "game_win_screen() must be implemented by the subclass."
        )

    def start_timer(self):
        """
        Start the timer for periodic updates.
        """
        self.timer.init(
            period=self.update_period,
            mode=Timer.PERIODIC,
            callback=lambda t: self.update_state(t),
        )

    def stop_timer(self):
        """
        Stop the periodic timer.
        """
        self.timer.deinit()

    def run(self):
        """
        Main game loop.
        """
        self.initialize_game()
        self.start_timer()

        while True:
            pressed = self.input.get_pressed()
            if pressed:
                for direction in pressed:
                    self.handle_input(direction)
            self.render()
            if self.game_over_flag:
                self.stop_timer()
                self.game_over_screen()
                break
            if self.game_win_flag:
                self.stop_timer()
                self.game_win_screen()
                break
            time.sleep(0.05)
