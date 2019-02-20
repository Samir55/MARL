from math import gcd

import pygame
import numpy as np

from src.agent import Agent


class Environment:
    WINDOW_HEIGHT = 360
    WINDOW_WIDTH = 640
    CELL_LENGTH = gcd(WINDOW_HEIGHT, WINDOW_WIDTH)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (247, 240, 48)
    RED = (201, 16, 41)
    BLUE = (0, 0, 255)

    NUMBER_OF_OBJECTS = 30
    MAX_NUMBER_OF_AGENTS = 5

    ROBOT_LOADED = "assets/robot-pack/PNG/TOP view/robot_green.png"
    ROBOT_UN_LOADED = "assets/robot-pack/PNG/TOP view/robot_red.png"

    TARGET_FLAG = "assets/kenney_sportspack/PNG/Equipment/flag_checkered.png"

    PADDING = 5

    def __init__(self):
        pygame.init()

        self.game_window = pygame.display.set_mode((Environment.WINDOW_WIDTH, Environment.WINDOW_HEIGHT), 0, 32)

        # Initialize the agents number.
        self.agents = []
        for i in range(np.random.randint(1, Environment.MAX_NUMBER_OF_AGENTS)):
            self.agents.append(
                Agent(np.random.randint(0, Environment.WINDOW_WIDTH // Environment.CELL_LENGTH),
                      np.random.randint(0, Environment.WINDOW_HEIGHT // Environment.CELL_LENGTH)))

        # Initialize the grid.
        self.grid = np.zeros((Environment.WINDOW_HEIGHT, Environment.WINDOW_WIDTH))

        return

    def draw(self):
        # Fill window.
        self.game_window.fill(Environment.WHITE)

        # Draw the source box.
        pygame.draw.rect(self.game_window, Environment.RED,
                         (0, 0, 2 * Environment.CELL_LENGTH, 2 * Environment.CELL_LENGTH))
        # Draw the dest box.
        i, j = (
            Environment.WINDOW_HEIGHT - 2 * Environment.CELL_LENGTH,
            Environment.WINDOW_WIDTH - 2 * Environment.CELL_LENGTH
        )
        pygame.draw.rect(self.game_window, Environment.YELLOW,
                         (j, i, i + 2 * Environment.CELL_LENGTH, j + 2 * Environment.CELL_LENGTH))

        # Draw the grid.
        h, w = self.grid.shape

        for i in range(0, w, Environment.CELL_LENGTH):
            pygame.draw.line(self.game_window, Environment.BLACK, (i, 0),
                             (i, Environment.WINDOW_HEIGHT - 1))

        for j in range(0, h, Environment.CELL_LENGTH):
            pygame.draw.line(self.game_window, Environment.BLACK, (0, j), (Environment.WINDOW_WIDTH - 1, j))

        # Draw the agents.
        for agent in self.agents:
            robot_loaded = pygame.image.load(Environment.ROBOT_LOADED).convert_alpha()
            robot_loaded = pygame.transform.scale(robot_loaded,
                                                  (Environment.CELL_LENGTH - 2 * Environment.PADDING,
                                                   Environment.CELL_LENGTH - 2 * Environment.PADDING))
            robot_loaded_rect = (
                agent.pos[0] * Environment.CELL_LENGTH + Environment.PADDING,
                agent.pos[1] * Environment.CELL_LENGTH + Environment.PADDING)
            self.game_window.blit(robot_loaded, robot_loaded_rect)

        # Draw the target flag.
        flag = pygame.image.load(Environment.TARGET_FLAG).convert_alpha()
        flag = pygame.transform.scale(flag, (30, 30))

        flag_rect = (
            Environment.WINDOW_WIDTH - 2 * Environment.CELL_LENGTH,
            Environment.WINDOW_HEIGHT - 2 * Environment.CELL_LENGTH - Environment.PADDING
        )
        self.game_window.blit(flag, flag_rect)

        # Draw the score TODO.

        # Draw the balls TODO


        # Update pygame display(required).
        pygame.display.update()

        return

    def add_agent(self):
        # Add new agents.
        self.agents.append(
            Agent(np.random.randint(0, Environment.CELL_LENGTH), np.random.randint(0, Environment.CELL_LENGTH)))

        return
