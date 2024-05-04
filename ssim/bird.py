"""
This class represents a single bird in a flock
"""
# pylint: disable=no-member
from __future__ import annotations
from typing import List
from obstacle import Obstacle

import random
import pygame
import pygame.locals
import math

NUM_ENTITIES = 100
MAX_SPEED = 2
SEPARATION_DISTANCE = 25

COLLISION_EVENT = pygame.USEREVENT + 1

class Bird:
    """
    Attributes:
        position: bird's position vector
        velocity: bird's velocity vector
        size: bird's hit box size
    """
    def __init__(self, x, y, size, perception_radius):
        """
        Constructor
        """
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(MAX_SPEED)
        self.size = size
        self.perception_radius = perception_radius

    def update(self, flock: List[Bird], obstacles) -> None:
        """
        Update bird's position using flocking algorithm
        """
        self.position += self.velocity

        self.wrap_edges()

        avg_velocity = pygame.Vector2(0, 0)
        avg_position = pygame.Vector2(0, 0)
        avg_separation = pygame.Vector2(0, 0)
        num_neighbors = 0

        for other in flock:
            if other == self:
                continue

            distance_squared = self.distance_to(other)

            if distance_squared < self.perception_radius ** 2:
                avg_velocity += other.velocity
                avg_position += other.position

                if distance_squared < SEPARATION_DISTANCE ** 2:
                    diff = self.position - other.position
                    diff.scale_to_length(1 / distance_squared)
                    avg_separation += diff

                num_neighbors += 1

        if num_neighbors > 0:
            avg_velocity /= num_neighbors
            avg_position /= num_neighbors
            avg_separation /= num_neighbors

        self.velocity += avg_velocity * 0.02
        self.velocity += avg_position * 0.01
        self.velocity += avg_separation * 0.03

        self.avoid_obstacles(obstacles)

        self.dodge_obstacles(obstacles)

        self.velocity.scale_to_length(MAX_SPEED)

        self.check_collisions(obstacles, flock)

    def wrap_edges(self) -> None:
        """
        Move the bird to the other side of the screen if it goes off the boundaries
        """
        width, height = pygame.display.get_surface().get_size()
        if self.position.x < 0:
            self.position.x = width
        if self.position.y < 0:
            self.position.y = height
        if self.position.x > width:
            self.position.x = 0
        if self.position.y > height:
            self.position.y = 0

    def distance_to(self, other: Bird) -> float:
        """
        Calculate distance between two birds
        """
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        return dx ** 2 + dy ** 2

    def check_collisions(self, obstacles, flock: List[Bird]) -> None:
        """
        Check if a bird collided with an obstacle, if so, remove it from the list representing flock
        """
        for obstacle in obstacles:
            dx = self.position[0] - obstacle.position[0]
            dy = self.position[1] - obstacle.position[1]
            distance_squared = dx ** 2 + dy ** 2
            if distance_squared < (self.size + obstacle.radius) ** 2:
                flock.remove(self)
                pygame.event.post(pygame.event.Event(COLLISION_EVENT))
                return
    
    def avoid_obstacles(self, obstacles:List[Obstacle]):
        for obstacle in obstacles:
            dx = obstacle.position[0] - self.position[0]
            dy = obstacle.position[1] - self.position[1]
            self.velocity += pygame.Vector2(random.uniform(0.001, 0.005)*dx, random.uniform(0.001,0.005)*dy)

    def dodge_obstacles(self, obstacles:List[Obstacle]):
        for obstacle in obstacles:
            dx = obstacle.position[0] - self.position[0]
            dy = obstacle.position[1] - self.position[1]
            distance_to_obstacle = math.sqrt(dx ** 2 + dy ** 2) - obstacle.radius
            if distance_to_obstacle <= self.perception_radius:
                self.velocity += pygame.Vector2(random.uniform(-1,-2)*dx, random.uniform(-1,-2)*dy)
            