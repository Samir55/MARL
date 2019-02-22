import gym
from gym import error, spaces, utils
from gym.utils import seeding

from math import gcd

import pygame
import numpy as np


class MARLEnv(gym.Env):
    WINDOW_HEIGHT = 360
    WINDOW_WIDTH = 640
    CELL_LENGTH = gcd(WINDOW_HEIGHT, WINDOW_WIDTH)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (247, 240, 48)
    RED = (201, 16, 41)
    BLUE = (0, 0, 255)
    PADDING = 5

    NUMBER_OF_OBJECTS = 30
    MAX_NUMBER_OF_AGENTS = 5

    MIN_BALLS_COUNT = 10
    MAX_BALLS_COUNT = 20

    MIN_PITS_COUNT = 3
    MAX_PITS_COUNT = 10

    ROBOT_LOADED = "../assets/robot-pack/PNG/TOP view/robot_green.png"
    ROBOT_UN_LOADED = "../assets/robot-pack/PNG/TOP view/robot_red.png"

    TARGET_FLAG = "../assets/kenney_sportspack/PNG/Equipment/flag_checkered.png"
    BALL = "../assets/kenney_sportspack/PNG/Equipment/ball_soccer1.png"

    def __init__(self):
        pygame.init()

        self.game_window = pygame.display.set_mode((MARLEnv.WINDOW_WIDTH, MARLEnv.WINDOW_HEIGHT), 0, 32)

        self.grid = None
        self.agents = None
        self.source_balls = None
        self.target_balls = None
        self.pits_pos = None

        # Initialize the agents number.
        self.reset()

    def render(self, mode='human', close=False):
        # Fill window.
        self.game_window.fill(MARLEnv.WHITE)

        ############################
        # Draw the grid.
        ############################
        h, w = self.grid.shape

        for i in range(0, w, MARLEnv.CELL_LENGTH):
            pygame.draw.line(self.game_window, MARLEnv.BLACK, (i, 0),
                             (i, MARLEnv.WINDOW_HEIGHT - 1))

        for j in range(0, h, MARLEnv.CELL_LENGTH):
            pygame.draw.line(self.game_window, MARLEnv.BLACK, (0, j), (MARLEnv.WINDOW_WIDTH - 1, j))

        ############################
        # Draw the pits.
        ############################
        for pit_pos in self.pits_pos:
            pygame.draw.rect(self.game_window, MARLEnv.RED,
                             (pit_pos[0] * MARLEnv.CELL_LENGTH, pit_pos[1] * MARLEnv.CELL_LENGTH, MARLEnv.CELL_LENGTH,
                              MARLEnv.CELL_LENGTH))

        ############################
        # Draw the source and the dest boxes.
        ############################
        pygame.draw.rect(self.game_window, MARLEnv.BLUE,
                         (0, 0, 2 * MARLEnv.CELL_LENGTH, 2 * MARLEnv.CELL_LENGTH))

        i, j = (
            MARLEnv.WINDOW_HEIGHT - 2 * MARLEnv.CELL_LENGTH + 1,
            MARLEnv.WINDOW_WIDTH - 2 * MARLEnv.CELL_LENGTH + 1
        )
        pygame.draw.rect(self.game_window, MARLEnv.YELLOW,
                         (j, i, i + 2 * MARLEnv.CELL_LENGTH, j + 2 * MARLEnv.CELL_LENGTH))

        ############################
        # Draw the agents.
        ############################
        for agent in self.agents:
            if agent['loaded']:
                robot_img = pygame.image.load(MARLEnv.ROBOT_LOADED).convert_alpha()
            else:
                robot_img = pygame.image.load(MARLEnv.ROBOT_UN_LOADED).convert_alpha()
            robot_img = pygame.transform.scale(robot_img,
                                               (MARLEnv.CELL_LENGTH - 2 * MARLEnv.PADDING,
                                                MARLEnv.CELL_LENGTH - 2 * MARLEnv.PADDING))
            robot_img_rect = (
                agent['pos'][0] * MARLEnv.CELL_LENGTH + MARLEnv.PADDING,
                agent['pos'][1] * MARLEnv.CELL_LENGTH + MARLEnv.PADDING)
            self.game_window.blit(robot_img, robot_img_rect)

        ############################
        # Draw the target flag.
        ############################
        flag = pygame.image.load(MARLEnv.TARGET_FLAG).convert_alpha()
        flag = pygame.transform.scale(flag, (30, 30))

        flag_rect = (
            MARLEnv.WINDOW_WIDTH - 2 * MARLEnv.CELL_LENGTH,
            MARLEnv.WINDOW_HEIGHT - 2 * MARLEnv.CELL_LENGTH - MARLEnv.PADDING
        )
        self.game_window.blit(flag, flag_rect)

        ############################
        # Draw the items (balls).
        ############################
        for ball in self.source_balls:
            ball_img = pygame.image.load(MARLEnv.BALL).convert_alpha()

            # else:
            #     ball_x, ball_y = (
            #         np.random.randint(MARLEnv.WINDOW_WIDTH - 2 * MARLEnv.CELL_LENGTH,
            #                           MARLEnv.WINDOW_WIDTH - MARLEnv.PADDING),
            #         np.random.randint(MARLEnv.WINDOW_HEIGHT - 2 * MARLEnv.CELL_LENGTH,
            #                           MARLEnv.WINDOW_HEIGHT - MARLEnv.PADDING)
            #     )

            ball_rect = (ball['pos'][0], ball['pos'][1])

            self.game_window.blit(ball_img, ball_rect)

        ############################
        # Update pygame display(required).
        ############################
        pygame.display.update()

        return

    def step(self, action):
        """

        Parameters
        ----------
        action :

        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if action == 'LEFT':
            x = 1
        elif action == 'RIGHT':
            x = 2
        elif action == 'UP':
            x = 3
        elif action == 'DOWN':
            x = 4
        elif action == 'PICK_UP':
            x = 5
        elif action == 'DROP':
            x = 6

        return

    def reset(self):

        # Add pits.
        self.pits_pos = []
        for i in range(np.random.randint(MARLEnv.MIN_PITS_COUNT, MARLEnv.MAX_PITS_COUNT)):
            self.pits_pos.append(
                (
                    np.random.randint(3, MARLEnv.WINDOW_WIDTH // MARLEnv.CELL_LENGTH - 2),
                    np.random.randint(3, MARLEnv.WINDOW_HEIGHT // MARLEnv.CELL_LENGTH - 2)
                )
            )

        # Initialize the agents number.
        self.agents = []
        for i in range(np.random.randint(1, MARLEnv.MAX_NUMBER_OF_AGENTS)):
            x, y = (np.random.randint(0, MARLEnv.WINDOW_WIDTH // MARLEnv.CELL_LENGTH),
                    np.random.randint(0, MARLEnv.WINDOW_HEIGHT // MARLEnv.CELL_LENGTH))

            while (x, y) in self.pits_pos:
                x, y = (np.random.randint(0, MARLEnv.WINDOW_WIDTH // MARLEnv.CELL_LENGTH),
                        np.random.randint(0, MARLEnv.WINDOW_HEIGHT // MARLEnv.CELL_LENGTH))
            self.agents.append(
                {
                    'pos': (x, y),
                    'steps': 0,
                    'loaded': False
                }
            )

        # Initialize the grid.
        self.grid = np.zeros((MARLEnv.WINDOW_HEIGHT, MARLEnv.WINDOW_WIDTH))

        # Initialize the items(balls) parameters.
        self.source_balls = []

        for i in range(np.random.randint(MARLEnv.MIN_BALLS_COUNT, MARLEnv.MAX_BALLS_COUNT)):
            self.source_balls.append(
                {
                    'pos': (np.random.randint(0, MARLEnv.CELL_LENGTH * 2 - 2 * MARLEnv.PADDING),
                            np.random.randint(0, MARLEnv.CELL_LENGTH * 2 - 2 * MARLEnv.PADDING))
                }
            )

        self.target_balls = []

        return
