# collect_stars.py

from game_framework import Game
import random
import machine
import time


class CollectStars(Game):
    PLAYER_CHAR = "P"
    STAR_CHAR = "*"
    ZOMBIE_CHAR = "Z"
    WALL_CHAR = "&"
    END_CHAR = "E"
    EMPTY_CHAR = " "

    def __init__(
        self,
        map_width=16,
        map_height=8,
        num_zombies=2,
        num_walls=5,
        num_stars=5,
        zombie_move_period=1000,
    ):
        """
        Initialize the Collect Stars game with specific settings.

        :param map_width: Width of the game map in cells.
        :param map_height: Height of the game map in cells.
        :param num_zombies: Number of zombies to place on the map.
        :param num_walls: Number of internal walls/obstacles.
        :param num_stars: Number of stars to collect.
        :param zombie_move_period: Period (in milliseconds) for zombie movements.
        """
        super().__init__(map_width, map_height, update_period=zombie_move_period)
        self.player_pos = (self.map_height - 2, 1)
        self.goal_pos = (1, self.map_width - 2)
        self.zombies = []
        self.stars = []
        self.num_zombies = num_zombies
        self.num_walls = num_walls
        self.num_stars = num_stars

    def custom_randrange(self, a, b):
        """
        Custom randrange using random.getrandbits.

        :param a: Start of range (inclusive).
        :param b: End of range (exclusive).
        :return: Random integer between a and b-1.
        """
        return a + (random.getrandbits(16) % (b - a))

    def initialize_game(self):
        """
        Initialize the game state: map, player, goal, zombies, walls, and stars.
        """
        self.init_map()
        self.place_player()
        self.place_goal()
        self.place_zombies()
        self.place_walls()
        self.place_stars()
        self.render()

    def init_map(self):
        """
        Initialize the game map with empty spaces and borders.
        """
        self.game_map = [
            [self.EMPTY_CHAR for _ in range(self.map_width)]
            for _ in range(self.map_height)
        ]

    def place_player(self):
        """
        Place the player character on the map.
        """
        y, x = self.player_pos
        self.game_map[y][x] = self.PLAYER_CHAR

    def place_goal(self):
        """
        Place the goal on the map.
        """
        y, x = self.goal_pos
        self.game_map[y][x] = self.END_CHAR

    def place_zombies(self):
        """
        Randomly place zombies on the map, avoiding the player and goal positions.
        """
        for _ in range(self.num_zombies):
            while True:
                y = self.custom_randrange(1, self.map_height - 1)
                x = self.custom_randrange(1, self.map_width - 1)
                if (
                    self.game_map[y][x] == self.EMPTY_CHAR
                    and (y, x) != self.player_pos
                    and (y, x) != self.goal_pos
                ):
                    self.game_map[y][x] = self.ZOMBIE_CHAR
                    self.zombies.append([y, x])
                    break

    def place_walls(self):
        """
        Randomly place internal walls/obstacles on the map.
        """
        for _ in range(self.num_walls):
            while True:
                y = self.custom_randrange(1, self.map_height - 1)
                x = self.custom_randrange(1, self.map_width - 1)
                if (
                    self.game_map[y][x] == self.EMPTY_CHAR
                    and (y, x) != self.player_pos
                    and (y, x) != self.goal_pos
                    and [y, x] not in self.zombies
                ):
                    self.game_map[y][x] = self.WALL_CHAR
                    break

    def place_stars(self):
        """
        Randomly place stars on the map for the player to collect.
        """
        for _ in range(self.num_stars):
            while True:
                y = self.custom_randrange(1, self.map_height - 1)
                x = self.custom_randrange(1, self.map_width - 1)
                if (
                    self.game_map[y][x] == self.EMPTY_CHAR
                    and (y, x) != self.player_pos
                    and (y, x) != self.goal_pos
                    and [y, x] not in self.zombies
                    and [y, x] not in self.stars
                ):
                    self.game_map[y][x] = self.STAR_CHAR
                    self.stars.append([y, x])
                    break

    def handle_input(self, direction):
        """
        Handle player movement based on input direction.

        :param direction: Direction input by the user (e.g., 'left', 'right', 'up', 'down').
        """
        y, x = self.player_pos
        new_y, new_x = y, x
        if direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
        elif direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1

        # Check boundaries and walls
        if 0 < new_y < self.map_height - 1 and 0 < new_x < self.map_width - 1:
            if self.game_map[new_y][new_x] in [
                self.EMPTY_CHAR,
                self.END_CHAR,
                self.STAR_CHAR,
            ]:
                self.game_map[y][x] = self.EMPTY_CHAR
                if self.game_map[new_y][new_x] == self.END_CHAR:
                    self.game_win_flag = True
                elif self.game_map[new_y][new_x] == self.STAR_CHAR:
                    self.score += 10  # Increment score for collecting a star
                    self.stars.remove([new_y, new_x])
                self.player_pos = (new_y, new_x)
                self.game_map[new_y][new_x] = self.PLAYER_CHAR

    def update_state(self, timer):
        """
        Move zombies towards the player each timer tick.
        """
        new_zombies = []
        for z in self.zombies:
            y, x = z
            dy = self.player_pos[0] - y
            dx = self.player_pos[1] - x
            move_y = dy // abs(dy) if dy != 0 else 0
            move_x = dx // abs(dx) if dx != 0 else 0
            new_y = y + move_y
            new_x = x + move_x

            # Check boundaries and walls
            if not (0 < new_y < self.map_height - 1 and 0 < new_x < self.map_width - 1):
                new_y, new_x = y, x  # Zombie stays
            elif self.game_map[new_y][new_x] == self.WALL_CHAR:
                new_y, new_x = y, x  # Zombie stays

            # Check collision with player
            if (new_y, new_x) == self.player_pos:
                self.game_over_flag = True

            # Update zombie position
            if self.game_map[new_y][new_x] in [
                self.EMPTY_CHAR,
                self.PLAYER_CHAR,
                self.END_CHAR,
                self.STAR_CHAR,
            ]:
                self.game_map[y][x] = self.EMPTY_CHAR
                if self.game_map[new_y][new_x] not in [self.END_CHAR, self.STAR_CHAR]:
                    self.game_map[new_y][new_x] = self.ZOMBIE_CHAR
                z[0], z[1] = new_y, new_x
                new_zombies.append(z)
            else:
                new_zombies.append(z)
        self.zombies = new_zombies
        self.score += 1
        self.render()

    def render(self):
        """
        Render the current game state to the display.
        """
        self.display.update_display(self.game_map, self.score)

    def game_over_screen(self):
        """
        Display the game over screen and reset the device after a delay.
        """
        self.display.clear()
        self.display.draw_text("GAME OVER", 30, 20)
        self.display.draw_text(f"Score: {self.score}", 30, 30)
        self.display.show()
        time.sleep(3)
        machine.reset()

    def game_win_screen(self):
        """
        Display the game win screen and reset the device after a delay.
        """
        self.display.clear()
        self.display.draw_text("YOU WIN!", 35, 20)
        self.display.draw_text(f"Score: {self.score}", 35, 30)
        self.display.show()
        time.sleep(3)
        machine.reset()
