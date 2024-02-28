import pygame

from pygame.locals import KEYDOWN, K_ESCAPE

pygame.init()

screen = pygame.display.set_mode([500, 500])
running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        screen.fill((255, 255, 255))

        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        pygame.display.flip()

pygame.quit()