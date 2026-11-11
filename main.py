import math
import pygame
import auth

# Initialize Pygame and set up the window
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Clicker")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 64)

username = auth.run_login(screen, clock)
if username is None:     
    pygame.quit()
    raise SystemExit
pygame.display.set_caption(f"Space Idle - {username}")

# Initialize game variables
score = 0
center = (400, 300)
radius = 100
currency_per_click = 1
upgrade_cost = 10
upgrade_idle_cost = 10
level = 1
idle_rate = 0

upgrade_rect = pygame.Rect(50, 450, 200, 60)
upgrade_idle_rect = pygame.Rect(50, 600, 200, 60)

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
                score += currency_per_click

                # Check if the click is inside the upgrade button
            elif upgrade_rect.collidepoint(event.pos):
                if score >= upgrade_cost:
                    score -= upgrade_cost
                    currency_per_click += 1
                    upgrade_cost *= 2

            elif upgrade_idle_rect.collidepoint(event.pos):
                if score >= upgrade_idle_cost:
                    score -= upgrade_idle_cost
                    idle_rate += 1   
                    level += 1
                    upgrade_idle_cost *= 2


    dt = clock.tick(60) / 1000   # the / 1000 is the important part
    score += idle_rate * dt  # Add the idle rate to the score based on the time elapsed

    # Draw the circle and score
    screen.fill((10, 10, 30))
    pygame.draw.circle(screen, (80, 140, 255), center, radius)

    # Draw the upgrade button
    pygame.draw.rect(screen, (70, 70, 200), upgrade_rect)

    # Draw the upgrade_idle button
    pygame.draw.rect(screen, (100, 100, 255), upgrade_idle_rect)

    # Draw the score text
    text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
    uprade_text = font.render(f"Upgrade ({upgrade_cost})", True, (255, 255, 255))
    idle_text = font.render(f"Upgrade (Idle) ({upgrade_idle_cost})", True, (255, 255, 255))

    # Center the score text and draw it on the screen
    screen.blit(text, (400 - text.get_width() // 2, 100))
    screen.blit(uprade_text, (upgrade_rect.x + 10, upgrade_rect.y + 10))
    screen.blit(idle_text, (upgrade_idle_rect.x + 10, upgrade_idle_rect.y + 10))

    # Update the display and tick the clock
    pygame.display.flip()
    clock.tick(60)

pygame.quit()