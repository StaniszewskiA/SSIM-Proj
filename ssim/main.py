import pygame
import pygame.locals
from environment import Environment

pygame.init()

# Bird properties
bird_options = {
    "AMOUNT": 300,
    "SIZE": 5,
    "COLOR": (255, 0, 0),
    "PERCEPTION_RADIUS": 25,
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
    



