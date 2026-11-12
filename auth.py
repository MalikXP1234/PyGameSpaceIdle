"""Login and sign-up for Space Idle (US 1).

Accounts and progress are saved in players.json next to this file.
Passwords are never stored: only a salted PBKDF2 hash.
"""

import hashlib
import json
import os
import re
import secrets
import pygame

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "players.json")


def _load():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, DATA_FILE)


def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()


def sign_up(username, password, confirm):
    """Returns an error message, or None if the account was created."""
    username = username.strip()
    if not re.fullmatch(r"[A-Za-z0-9_]{3,16}", username):
        return "Username: 3-16 letters, numbers or _"
    if len(password) < 6:
        return "Password must be at least 6 characters"
    if password != confirm:
        return "Passwords do not match"
    data = _load()
    if username.lower() in data:
        return "That username is taken"
    salt = secrets.token_hex(16)
    data[username.lower()] = {"name": username, "salt": salt, "hash": _hash(password, salt), "progress": {}}
    _save(data)
    return None


def log_in(username, password):
    """Returns an error message, or None if the details are correct."""
    user = _load().get(username.strip().lower())
    # Same message either way, so nobody can find out which usernames exist
    if not user or not secrets.compare_digest(user["hash"], _hash(password, user["salt"])):
        return "Wrong username or password"
    return None


def load_progress(username):
    user = _load().get(username.lower(), {})
    return user.get("progress", {})


def save_progress(username, progress):
    data = _load()
    if username.lower() in data:
        data[username.lower()]["progress"] = progress
        _save(data)

BG = (16, 18, 32)
PANEL = (30, 34, 56)
FIELD = (44, 50, 78)
ACTIVE = (120, 170, 255)
TEXT = (235, 238, 245)
MUTED = (150, 158, 180)
ERROR = (255, 110, 110)
GOOD = (120, 220, 150)
BUTTON = (90, 130, 255)


class InputBox:
    def __init__(self, label, rect, secret=False):
        self.label, self.rect, self.secret = label, pygame.Rect(rect), secret
        self.text, self.active = "", False

    def handle(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.text) < 24:
                self.text += event.unicode

    def draw(self, screen, font, small):
        screen.blit(small.render(self.label, True, MUTED), (self.rect.x, self.rect.y - 24))
        pygame.draw.rect(screen, FIELD, self.rect, border_radius=8)
        pygame.draw.rect(screen, ACTIVE if self.active else FIELD, self.rect, 2, border_radius=8)
        shown = "*" * len(self.text) if self.secret else self.text
        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            shown += "|"
        screen.blit(font.render(shown, True, TEXT), (self.rect.x + 12, self.rect.y + 12))


def run_login(screen, clock):
    """Shows the login / sign-up screen. Returns the username, or None if the window is closed."""
    w, h = screen.get_size()
    title_font = pygame.font.SysFont(None, 64)
    font = pygame.font.SysFont(None, 32)
    small = pygame.font.SysFont(None, 24)

    px, pw = w // 2 - 220, 440
    tabs = {"login": pygame.Rect(px, 190, pw // 2, 44), "signup": pygame.Rect(px + pw // 2, 190, pw // 2, 44)}
    user_box = InputBox("Username", (px + 30, 290, pw - 60, 46))
    pass_box = InputBox("Password", (px + 30, 375, pw - 60, 46), secret=True)
    confirm_box = InputBox("Confirm password", (px + 30, 460, pw - 60, 46), secret=True)
    mode, message, msg_colour = "login", "", ERROR

    def boxes():
        return [user_box, pass_box] + ([confirm_box] if mode == "signup" else [])

    def focus(box):
        for b in (user_box, pass_box, confirm_box):
            b.active = b is box

    focus(user_box)

    def submit():
        nonlocal message, msg_colour, mode
        if mode == "login":
            err = log_in(user_box.text, pass_box.text)
            if err:
                message, msg_colour = err, ERROR
                return None
            return user_box.text.strip()
        err = sign_up(user_box.text, pass_box.text, confirm_box.text)
        if err:
            message, msg_colour = err, ERROR
            return None
        message, msg_colour, mode = "Account created. Please log in.", GOOD, "login"
        pass_box.text = confirm_box.text = ""
        focus(pass_box)
        return None

    while True:
        button = pygame.Rect(px + 30, 545 if mode == "signup" else 460, pw - 60, 52)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in tabs.items():
                    if rect.collidepoint(event.pos) and mode != name:
                        mode, message = name, ""
                        focus(user_box)
                for b in boxes():
                    if b.rect.collidepoint(event.pos):
                        focus(b)
                if button.collidepoint(event.pos):
                    result = submit()
                    if result:
                        return result
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result = submit()
                    if result:
                        return result
                elif event.key == pygame.K_TAB:  # move to the next field
                    bs = boxes()
                    i = next((k for k, b in enumerate(bs) if b.active), -1)
                    focus(bs[(i + 1) % len(bs)])
                else:
                    for b in boxes():
                        b.handle(event)

        screen.fill(BG)
        t = title_font.render("SPACE IDLE", True, TEXT)
        screen.blit(t, (w // 2 - t.get_width() // 2, 100))
        panel_h = 470 if mode == "signup" else 385
        pygame.draw.rect(screen, PANEL, (px, 190, pw, panel_h), border_radius=14)
        for name, rect in tabs.items():
            on = mode == name
            pygame.draw.rect(screen, FIELD if on else PANEL, rect, border_radius=14)
            label = font.render("Log in" if name == "login" else "Sign up", True, TEXT if on else MUTED)
            screen.blit(label, label.get_rect(center=rect.center))
        for b in boxes():
            b.draw(screen, font, small)
        hover = button.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (110, 150, 255) if hover else BUTTON, button, border_radius=10)
        lbl = font.render("Log in" if mode == "login" else "Create account", True, TEXT)
        screen.blit(lbl, lbl.get_rect(center=button.center))
        if message:
            m = small.render(message, True, msg_colour)
            screen.blit(m, (w // 2 - m.get_width() // 2, button.bottom + 16))
        hint = small.render("Tab: next field   Enter: submit", True, MUTED)
        screen.blit(hint, (w // 2 - hint.get_width() // 2, h - 60))
        pygame.display.flip()
        clock.tick(60)
