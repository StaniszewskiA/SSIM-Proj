import pygame
import pygame.locals
import os
import random
from environment import Environment
from pylint_runner import run_pylint_on_folder

def main():
    pygame.init()

    DISPLAY_INFO = pygame.display.Info()
    RUNNING = True

    # Bird properties
    bird_options = {
        "AMOUNT": 100,
        "SIZE": 5,
        "COLOR": (255, 0, 0),
        "PERCEPTION_RADIUS": [25, 75],
    }

    min_x = 0
    max_x = 1366
    min_y = 0
    max_y = 768
    random_positions = [(random.randint(min_x, max_x), random.randint(min_y, max_y)) for _ in range(10)]

    # Obstacle properties
    obstacle_options = {
        "RADIUS" : 50,
        "COLOR" : (0, 255, 0),
        "POSITIONS": random_positions
    }

    # Screen properties
    screen_options = {
        'WIDTH' : 1366,
        'HEIGHT' : 768
    }

    # Environment properties
    environment = Environment(
        bird_options=bird_options,
        obstacle_options=obstacle_options,
        screen_options=screen_options,
        clock=pygame.time.Clock())

    environment.start()

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
    
if __name__ == "__main__":
    #current_folder = os.path.dirname(os.path.abspath(__file__))
    #run_pylint_on_folder(current_folder)
    main()
