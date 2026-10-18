import math
import pygame

# Initialize Pygame and set up the window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Clicker")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 64)

# Initialize game variables
score = 0
center = (400, 300)
radius = 100

# Set up the main game loop
running = True
while running:
    for event in pygame.event.get():
        # Handle quitting the game
        if event.type == pygame.QUIT:
            running = False

    # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # Check if the click is inside the circle
            if math.hypot(mx - center[0], my - center[1]) <= radius:
                score += 1

    # Draw the circle and score
    screen.fill((10, 10, 30))
    pygame.draw.circle(screen, (80, 140, 255), center, radius)

    # Draw the score text
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (400 - text.get_width() // 2, 100))

    # Update the display and tick the clock
    pygame.display.flip()
    clock.tick(60)

pygame.quit()