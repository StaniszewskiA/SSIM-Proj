"""
Driver code for the simulation
"""
# pylint: disable=no-member

import random
import pygame
import pygame.locals

from bird import Bird

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flock Simulation")

# Ball properties
BIRD_AMOUNT = 100
BIRD_SIZE = 5
BIRD_COLOR = (255, 0, 0)
BIRD_SPEED = 5

birds = [Bird((random.randint(0, width), random.randint(0, height)),
            BIRD_SIZE, BIRD_COLOR, BIRD_SPEED) for i in range(BIRD_AMOUNT)]

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
    for bird in birds:
        bird.move(keys, (width, height))

    for i in range(BIRD_AMOUNT):
        for j in range(i + 1, BIRD_AMOUNT):
            birds[i].avoid_colision(birds[j])

    screen.fill((255, 255, 255))

    for bird in birds:
        bird.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
