"""
This class represents a single bird in a flock
"""
# pylint: disable=no-member
from __future__ import annotations
from typing import Tuple

import math
import pygame
import pygame.locals
import random

NUM_ENTITIES = 100
MAX_SPEED = 2
PERCEPTION_RADIUS = 50
SEPARATION_DISTANCE = 25


class Bird:
    """
    Attributes:
        x: x-coordinate of the bird
        y: y-coordinate of the bird
    """
    def __init__(self, x, y):
        """
        Constructor
        """
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(MAX_SPEED)

    def update(self, flock):
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

            if distance_squared < PERCEPTION_RADIUS ** 2:
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

        self.velocity.scale_to_length(MAX_SPEED)

    def wrap_edges(self):
        width, height = pygame.display.get_surface().get_size()
        if self.position.x < 0:
            self.position.x = width
        if self.position.y < 0:
            self.position.y = height
        if self.position.x > width:
            self.position.x = 0
        if self.position.y > height:
            self.position.y = 0

    def distance_to(self, other):
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        return dx ** 2 + dy ** 2
