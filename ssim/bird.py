"""
This class represents a single bird in a flock
"""

# pylint: disable=no-name-in-module
from __future__ import annotations
from typing import Tuple

import math
from pygame.locals import K_RIGHT, K_LEFT, K_DOWN, K_UP

import pygame


class Bird:
    """
    Attributes:
        x: x-coordinate of the bird
        y: y-coordinate of the bird
        radius: radius of the bird
        color: color of the bird
        speed: speed of the bird
    """
    def __init__(self, coords: Tuple[int, int], radius: int,
                 color: Tuple[int, int, int], speed: int):
        """
        Constructor
        """
        self.x = coords[0]
        self.y = coords[1]
        self.radius = radius
        self.color = color
        self.speed = speed

    def move(self, keys: pygame.key, bounds: Tuple[int, int]) -> None:
        """
        Move the bird based on the keys pressed.

        Args:
            keys: PyGame key input
            bounds: Tuple representing the screen bounds
        """
        self.x += (keys[K_RIGHT] - keys[K_LEFT]) * self.speed
        self.y += (keys[K_DOWN] - keys[K_UP]) * self.speed
        self.x = max(self.radius, min(bounds[0] - self.radius, self.x))
        self.y = max(self.radius, min(bounds[1] - self.radius, self.y))

    def avoid_colision(self, collider: Bird) -> None:
        """
        Adjust positions to avoid colliding with other birds.

        Args:
            collider: Another bird instance.
        """
        dx = self.x - collider.x
        dy = self.y - collider.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < self.radius + collider.radius:
            overlap = (self.radius + collider.radius - distance) / 2
            direction = math.atan2(dx, dy)

            self.x -= overlap * math.cos(direction)
            self.y -= overlap * math.sin(direction)
            collider.x += overlap * math.cos(direction)
            collider.y += overlap * math.sin(direction)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the bird on the screen

        Args:
            screen: PyGame surface to draw the bird on.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
