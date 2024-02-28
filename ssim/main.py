import pygame

from pygame.locals import KEYDOWN, K_ESCAPE

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flock Simulation")

# Ball properties
ball_radius = 20
ball_color = (255, 0, 0)
ball_speed = 5

# Initial position
ball_x, ball_y = width // 2, height // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update position
    keys = pygame.key.get_pressed()
    ball_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * ball_speed
    ball_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * ball_speed

    # Check boundaries
    ball_x = max(ball_radius, min(width - ball_radius, ball_x))
    ball_y = max(ball_radius, min(height - ball_radius, ball_y))

    # Backgroung
    screen.fill((255, 255, 255))

    # Ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Update display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
