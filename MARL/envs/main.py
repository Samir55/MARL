import sys

import pygame

from MARL.envs.marl_env import MARLEnv

if __name__ == "__main__":

    print("Creating the environment")
    running = True
    e = MARLEnv()

    while running:
        # Check for events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    e.step(0)
                elif event.key == pygame.K_RIGHT:
                    e.step(1)
                elif event.key == pygame.K_UP:
                    e.step(2)
                elif event.key == pygame.K_DOWN:
                    e.step(3)
                elif event.key == pygame.K_p:
                    e.step(4)
                elif event.key == pygame.K_d:
                    e.step(5)

        e.render()

        # Temproraly update the agent position for testing
        # e.agents[0].pos = (e.agents[0].pos[0] + 1, e.agents[0].pos[1])

        # Add some delay to see the drawing.
        pygame.time.delay(100)

    pygame.quit()
    sys.exit()
