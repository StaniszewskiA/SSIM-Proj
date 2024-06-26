"""
This class represents an obstacle
"""
from __future__ import annotations
from dataclasses import dataclass

import pygame
import pygame.locals


@dataclass
class Obstacle:
    """
    Attributes:
        x: x-coordinate of the obstacle's center
        y: y-coordinate of the obstacle's center
    """
    def __init__(self, x, y, radius, screen):
        self.position = (x, y)
        self.screen = screen
        self.radius = radius
