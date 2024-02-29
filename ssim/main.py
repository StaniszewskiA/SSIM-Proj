import pygame

from bird import Bird

from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flock Simulation")

# Ball properties
bird_amount = 5
bird_radius = 20
bird_color = (255, 0, 0)
bird_speed = 5

birds = [Bird(width // 2 + 30 * i, height // 2 + 30 * i, bird_radius, bird_color, bird_speed)
         for i in range(bird_amount)]

clock = pygame.time.Clock()
running = True

def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
    return True

while running:
    running = handle_events()

    keys = pygame.key.get_pressed()
    for bird in birds:
        bird.move(keys, (width, height))

    screen.fill((255, 255, 255))

    for bird in birds:
        bird.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
