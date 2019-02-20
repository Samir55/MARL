import sys

import pygame

from src.environment import Environment

if __name__ == "__main__":

    print("Creating the environment")
    running = True
    e = Environment()

    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        e.draw()

        # Temproraly update the agent position for testing
        # e.agents[0].pos = (e.agents[0].pos[0] + 1, e.agents[0].pos[1])

        # Add some delay to see the drawing.
        pygame.time.delay(100)

    pygame.quit()
    sys.exit()
