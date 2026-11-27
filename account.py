
import pygame
from auth import load_progress, save_progress

BG = (16, 18, 32)
PANEL = (30, 34, 56)
TEXT = (235, 238, 245)
BUTTON = (90, 130, 255)


def account_page(screen, clock, username, progress):
    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 55)

    width, height = screen.get_size()

    save_button = pygame.Rect(width // 2 - 150, 510, 300, 50)
    logout_button = pygame.Rect(width // 2 - 150, 580, 300, 50)
    back_button = pygame.Rect(30, 30, 120, 45)

    message = ""

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if save_button.collidepoint(event.pos):
                        save_progress(username, progress)
                        message = "Progress saved!"

                    if logout_button.collidepoint(event.pos):
                        save_progress(username, progress)
                        return "logout"

                    if back_button.collidepoint(event.pos):
                        return "back"

        screen.fill(BG)

        title = title_font.render("My Account", True, TEXT)
        screen.blit(title, title.get_rect(center=(width // 2, 100)))

        pygame.draw.rect(
            screen, PANEL,
            (width // 2 - 220, 160, 440, 300),
            border_radius=12
        )

        details = [
            "Username: " + username,
            "Credits: " + str(progress.get("credits", 0)),
            "Level: " + str(progress.get("level", 1)),
            "Click Power: " + str(progress.get("click_power", 1))
        ]

        for i, detail in enumerate(details):
            label = font.render(detail, True, TEXT)
            screen.blit(label, (width // 2 - 180, 210 + i * 55))

        pygame.draw.rect(screen, BUTTON, save_button, border_radius=8)
        pygame.draw.rect(screen, BUTTON, logout_button, border_radius=8)
        pygame.draw.rect(screen, PANEL, back_button, border_radius=8)

        save_text = font.render("Save Progress", True, TEXT)
        logout_text = font.render("Log Out", True, TEXT)
        back_text = font.render("Back", True, TEXT)

        screen.blit(save_text, save_text.get_rect(center=save_button.center))
        screen.blit(logout_text, logout_text.get_rect(center=logout_button.center))
        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        if message:
            msg = font.render(message, True, (120, 220, 150))
            screen.blit(msg, msg.get_rect(center=(width // 2, 680)))

        pygame.display.flip()
        clock.tick(60)
