import pygame

class Bird:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

    def move(self, keys, bounds):
        self.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        self.x = max(self.radius, min(bounds[0] - self.radius, self.x))
        self.y = max(self.radius, min(bounds[1] - self.radius, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
