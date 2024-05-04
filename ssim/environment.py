import pygame
import random

from bird import Bird, COLLISION_EVENT
from obstacle import Obstacle
from typing import List, Dict


class Environment():
    def __init__(
            self, 
            bird_options:Dict, 
            obstacle_options:Dict,
            screen_options:Dict, 
            clock:pygame.time.Clock
            ):
        """
        Constructor
        """
        self.flock = []
        self.bird_options = bird_options
        self.obstacles = []
        self.obstacle_options = obstacle_options
        self.clock = clock
        self.screen_options = screen_options
        self.screen = pygame.display.set_mode((self.screen_options['WIDTH'], self.screen_options['HEIGHT']))
        self.running = True
        self.keys = None
        self.visualize_perception_radius_flock: bool = False
        self.visualize_perception_radius_obstacle: bool = True
        self.reset_cooldown: int = 1000
        self.last_reset_time: int = 0
    
    def setup_display(self):
        """
        Setting up the display
        """
        pygame.display.set_caption("Flock simulation")
        return
    
    def handle_events(self):
        """
        Handle events in the simulation
        """
        for event in pygame.event.get():
            if (event.type == pygame.locals.QUIT
                    or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE)):
                self.running = False
            elif event.type == COLLISION_EVENT:
                self.spawn_new_bird(
                    x = random.randint(0, self.screen_options['WIDTH']),
                    y = random.randint(0, self.screen_options['HEIGHT']),
                    size=self.bird_options['SIZE'],
                    perception_radius=self.bird_options['PERCEPTION_RADIUS']
                )

    def start(self):
        self.setup_display()

        for _ in range(self.bird_options['AMOUNT']):
            self.spawn_new_bird(
                x = random.randint(0, self.screen_options['WIDTH']),
                y = random.randint(0, self.screen_options['HEIGHT']),
                size = self.bird_options['SIZE'],
                perception_radius = self.bird_options['PERCEPTION_RADIUS']
            )
        
        for i in range(len(self.obstacle_options['POSITIONS'])):
            self.spawn_new_obstacle(
                x = self.obstacle_options['POSITIONS'][i][0],
                y = self.obstacle_options['POSITIONS'][i][1],
                screen = self.screen
            )


    def spawn_new_bird(self, x:float, y:float, size:float, perception_radius: List[int]):
        """
        Spawn new birds
        """
        self.flock.append(Bird(x, y, size, perception_radius))
    
    def spawn_new_obstacle(self, x:float, y:float, screen:pygame.display):
        """
        Spawn new obstacle
        """
        self.obstacles.append(Obstacle(x, y, self.obstacle_options['RADIUS'], screen))

    def update_birds(self):
        for bird in self.flock:
            bird.update(flock=self.flock, obstacles=self.obstacles)
    
    def draw_birds(self):
        for bird in self.flock:
            pygame.draw.circle(
                self.screen, 
                (255, 255, 255), 
                (int(bird.position.x), int(bird.position.y)), 
                bird.size)
            if self.visualize_perception_radius_flock:
                if bird.has_neighbors:
                    pygame.draw.circle(self.screen, (0, 255, 0), (int(bird.position.x), int(bird.position.y)),
                                    bird.perception_radius_flock, 1)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(bird.position.x), int(bird.position.y)),
                                    bird.perception_radius_flock, 1)
            if self.visualize_perception_radius_obstacle:
                if not bird.approaching_obstacle:
                    pygame.draw.circle(self.screen, (0, 255, 0), (int(bird.position.x), int(bird.position.y)),
                                        bird.perception_radius_obstacle, 1)
                else: 
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(bird.position.x), int(bird.position.y)),
                                        bird.perception_radius_obstacle, 1)
    
    def draw_obstacles(self):
        for obstacle in self.obstacles:
            pygame.draw.circle(
                self.screen, 
                (self.obstacle_options['COLOR']), 
                (obstacle.position[0], obstacle.position[1]), 
                obstacle.radius)
    
    def check_keys(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_r]:
            current_time = pygame.time.get_ticks()
            if current_time - self.reset_cooldown > self.last_reset_time:
                self.reset_simulation()
                self.last_reset_time = current_time


    def reset_simulation(self):
        self.flock.clear()
        self.obstacles.clear()

        self.start()
