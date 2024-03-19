"""
Driver code for the simulation
"""
# pylint: disable=no-member

import random
import pygame
import pygame.locals

from typing import List
from bird import Bird
from obstacle import Obstacle
from environment import Environment

pygame.init()

# Set up display
# screen = pygame.display.set_mode((0, 0))
# width, height = pygame.display.get_surface().get_size()
# pygame.display.set_caption("Flock Simulation")


# Initial placement of th birds should be changed to follow flocking algorithm
# birds: List[Bird] = [Bird(random.randint(0, width), random.randint(0, height), bird_options["SIZE"])
#                      for i in range(bird_options["AMOUNT"])]
# obstacles = []

# RUNNING = True

# clock = pygame.time.Clock()


# def handle_events():
#     """
#     Handle closing the simulation
#     """
#     for event in pygame.event.get():
#         if (event.type == pygame.locals.QUIT
#                 or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE)):
#             return False

#     return True


# while RUNNING:
#     RUNNING = handle_events()

#     keys = pygame.key.get_pressed()

#     screen.fill((0, 0, 0))

#     obstacles.append(Obstacle(250, 250, screen))
#     obstacles.append(Obstacle(750, 750, screen))

#     for bird in birds:
#         bird.update(flock=birds, obstacles=obstacles)
#         pygame.draw.circle(screen, (255, 255, 255), (int(bird.position.x), int(bird.position.y)), 3)

#     for obstacle in obstacles:
#         obstacle.draw()

#     pygame.display.flip()

#     clock.tick(60)

# pygame.quit()

pygame.init()

# Bird properties
bird_options = {
    "AMOUNT": 300,
    "SIZE": 5,
    "COLOR": (255, 0, 0),
}

obstacle_options = {
    "RADIUS" : 100,
    "COLOR" : (0, 255, 0),
    "POSITIONS": [(250, 250), (750, 750)]
}

screen_options = {
    'WIDTH' : 1366,
    'HEIGHT' : 768
}

environment = Environment(
    bird_options=bird_options,
    obstacle_options=obstacle_options,
    screen_options=screen_options,
    clock=pygame.time.Clock())

environment.start()

RUNNING = True

while RUNNING:
    environment.screen.fill((0,0,0))

    RUNNING = environment.running

    environment.check_keys()

    environment.handle_events()

    environment.draw_obstacles()

    environment.update_birds()

    environment.draw_birds()

    pygame.display.flip()

    environment.clock.tick(60)

pygame.quit()
    



