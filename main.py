import math
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Clicker")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 64)

score = 0
center = (400, 300)
radius = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if math.hypot(mx - center[0], my - center[1]) <= radius:
                score += 1

    screen.fill((10, 10, 30))
    pygame.draw.circle(screen, (80, 140, 255), center, radius)

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (400 - text.get_width() // 2, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()