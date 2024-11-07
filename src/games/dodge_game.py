# dodge_game.py

from game_framework import Game
import random
import machine
import time


class DodgeGame(Game):
    """
    Dodge the Falling Objects Game
    ====================================
    The player controls a character at the bottom of the screen,
    moving left and right to dodge objects falling from the top.
    """

    # Define ASCII characters for game elements
    PLAYER_CHAR = "A"  # Player representation
    OBJECT_CHAR = "O"  # Falling object representation
    WALL_CHAR = "#"  # Wall or boundary representation
    EMPTY_CHAR = " "  # Empty space

    def __init__(
        self,
        map_width=16,
        map_height=8,
        num_walls=1,
        object_spawn_interval=1,  # Reduced interval for testing
        object_fall_speed=1,
    ):
        """
        Initialize the DodgeGame with specific settings.

        :param map_width: Width of the game map in cells.
        :param map_height: Height of the game map in cells.
        :param num_walls: Number of walls to place on each side.
        :param object_spawn_interval: Time interval (in seconds) between object spawns.
        :param object_fall_speed: Number of cells an object falls per update.
        """
        super().__init__(map_width, map_height, update_period=300)
        self.player_pos = (
            self.map_height - 1,
            self.map_width // 2,
        )
        self.objects = []
        self.score = 0
        self.num_walls = num_walls
        self.object_spawn_interval = object_spawn_interval
        self.object_fall_speed = object_fall_speed
        self.last_spawn_time = time.ticks_ms()

    def initialize_game(self, initial_objects=3):
        """
        Initialize the game state: map, player, and objects.
        """
        self.init_map()
        self.place_player()
        for _ in range(initial_objects):
            self.spawn_object()
        self.render()

    def init_map(self):
        """
        Initialize the game map with empty spaces and walls.
        """
        self.game_map = [
            [self.EMPTY_CHAR for _ in range(self.map_width)]
            for _ in range(self.map_height)
        ]

        # Place walls on the left and right edges
        for y in range(self.map_height):
            for wall in range(self.num_walls):
                self.game_map[y][wall] = self.WALL_CHAR
                self.game_map[y][self.map_width - 1 - wall] = self.WALL_CHAR

    def place_player(self):
        """
        Place the player character on the map.
        """
        y, x = self.player_pos
        self.game_map[y][x] = self.PLAYER_CHAR

    def custom_randrange(self, start, stop=None, step=1):
        """
        Emulate Python's randrange function using random.getrandbits().

        :param start: Start of range (inclusive).
        :param stop: End of range (exclusive). If None, start is treated as stop and start is set to 0.
        :param step: Step size. Defaults to 1.
        :return: Random integer from the range.
        """
        if stop is None:
            stop = start
            start = 0

        range_size = (stop - start) // step
        if range_size <= 0:
            raise ValueError("Empty range for randrange")

        random_value = random.getrandbits(16) % range_size
        return start + step * random_value

    def custom_randint(self, start, stop):
        """
        Emulate Python's randint function using custom_randrange.

        :param start: Start of range (inclusive).
        :param stop: End of range (inclusive).
        :return: Random integer between start and stop.
        """
        return self.custom_randrange(start, stop + 1)

    def spawn_object(self):
        """
        Spawn a new falling object at a random horizontal position.
        """

        min_x = self.num_walls
        max_x = self.map_width - self.num_walls - 1
        x = self.custom_randrange(min_x, max_x + 1)
        y = 0

        # Avoid spawning on the player
        if (y, x) == self.player_pos:
            return

        # Avoid spawning on existing objects
        for obj in self.objects:
            if obj["x"] == x and obj["y"] == y:
                return

        self.objects.append({"y": y, "x": x})
        self.game_map[y][x] = self.OBJECT_CHAR

    def handle_input(self, direction):
        """
        Handle player movement based on input direction.

        :param direction: Direction input by the player
        """
        y, x = self.player_pos
        new_x = x

        if direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1

        # Check boundaries and walls
        min_x = self.num_walls
        max_x = self.map_width - self.num_walls - 1

        if min_x <= new_x <= max_x:
            self.game_map[y][x] = self.EMPTY_CHAR
            self.player_pos = (y, new_x)
            self.game_map[y][new_x] = self.PLAYER_CHAR

    def update_state(self, timer):
        """
        Update the game state: spawn objects, move existing objects, check for collisions.

        :param timer: Timer tick (unused).
        """
        current_time = time.ticks_ms()

        # Spawn new object at intervals
        if (
            time.ticks_diff(current_time, self.last_spawn_time)
            > self.object_spawn_interval * 1000
        ):
            self.spawn_object()
            self.last_spawn_time = current_time

        # Move objects
        objects_to_remove = []
        for obj in self.objects:
            y = obj["y"]
            x = obj["x"]

            # Clear current position
            self.game_map[y][x] = self.EMPTY_CHAR

            # Move object down by fall_speed
            new_y = y + self.object_fall_speed

            if new_y >= self.map_height:
                self.score += 1
                objects_to_remove.append(obj)
                continue

            # Check collision with player
            if (new_y, x) == self.player_pos:
                self.game_over_flag = True
                return

            # Place object in new position
            if self.game_map[new_y][x] == self.EMPTY_CHAR:
                self.game_map[new_y][x] = self.OBJECT_CHAR
                obj["y"] = new_y
            else:
                # Collision with another object or wall
                self.game_over_flag = True
                return

        # Remove objects that have fallen past the bottom
        for obj in objects_to_remove:
            self.objects.remove(obj)

        # Render the updated state after all updates
        self.render()

    def render(self):
        """
        Render the current game state to the display.
        """
        self.display.clear()

        # Draw the game map
        for y in range(self.map_height):
            for x in range(self.map_width):
                char = self.game_map[y][x]
                if char == self.OBJECT_CHAR:
                    self.display.draw_text(char, x * 8, y * 8)
                elif char == self.PLAYER_CHAR:
                    self.display.draw_text(char, x * 8, y * 8)
                elif char == self.WALL_CHAR:
                    self.display.draw_text(char, x * 8, y * 8)
                # No need to draw EMPTY_CHAR

        # Draw the score
        score_text = f"Score: {self.score}"
        self.display.draw_text(score_text, 0, 0)

        self.display.show()

    def game_over_screen(self):
        """
        Display the game over screen with the final score and reset after a delay.
        """
        self.display.clear()
        game_over_text = "GAME OVER"
        score_text = f"Final Score: {self.score}"
        self.display.draw_text(game_over_text, 20, 25)
        self.display.draw_text(score_text, 20, 35)
        self.display.show()
        time.sleep(3)
        machine.reset()

    def game_win_screen(self):
        """
        TODO: Implement a game win screen
        """
        pass
