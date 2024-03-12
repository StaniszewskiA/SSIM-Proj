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

pygame.init()

# Set up display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("Flock Simulation")

# Bird properties
bird_options = {
    "AMOUNT": 300,
    "SIZE": 5,
    "COLOR": (255, 0, 0),
}

# Initial placement of th birds should be changed to follow flocking algorithm
birds: List[Bird] = [Bird(random.randint(0, width), random.randint(0, height), bird_options["SIZE"])
                     for i in range(bird_options["AMOUNT"])]
obstacles = []

RUNNING = True

clock = pygame.time.Clock()


def handle_events():
    """
    Handle closing the simulation
    """
    for event in pygame.event.get():
        if (event.type == pygame.locals.QUIT
                or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE)):
            return False

    return True


while RUNNING:
    RUNNING = handle_events()

    keys = pygame.key.get_pressed()

    screen.fill((0, 0, 0))

    obstacles.append(Obstacle(250, 250, screen))
    obstacles.append(Obstacle(750, 750, screen))

    for bird in birds:
        bird.update(flock=birds, obstacles=obstacles)
        pygame.draw.circle(screen, (255, 255, 255), (int(bird.position.x), int(bird.position.y)), 3)

    for obstacle in obstacles:
        obstacle.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()