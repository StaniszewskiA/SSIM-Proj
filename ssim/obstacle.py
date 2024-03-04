"""
This class represents an obstacle
"""
from __future__ import annotations

import pygame
import pygame.locals


class Obstacle:
    """
    Attributes:
        x: x-coordinate of the obstacle's center
        y: y-coordinate of the obstacle's center
    """
    def __init__(self, x, y, screen):
        self.position = (x, y)
        self.screen = screen
        self.radius = 100

    def draw(self) -> None:
        """
        Draw obstacle into the screen
        :return:
        """
        pygame.draw.circle(self.screen, (0, 255, 0),(int(self.position[0]),
                            int(self.position[1])), self.radius)
