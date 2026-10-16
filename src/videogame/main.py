import pygame

from videogame import settings
from videogame.entities import Chaser, Cookie, Player

MODES = [
    ("Classic", "Eat cookies at your own pace."),
    ("Challenge", f"{settings.CHALLENGE_TIME} seconds. Avoid burnt cookies and the angry ones!"),
]


class Round:
    """One play-through of a mode, from start until time runs out or the player is caught."""

    def __init__(self, mode):
        self.mode = mode
        self.challenge = mode == "Challenge"
        self.player = Player(settings.WIDTH / 2, settings.HEIGHT / 2)
        self.cookies = [self.new_cookie() for _ in range(settings.COOKIE_COUNT)]
        self.score = 0
        self.result = None  # set to a message when the round ends
        if self.challenge:
            self.cookies += [self.new_cookie(burnt=True) for _ in range(settings.BURNT_COUNT)]
            self.chasers = [Chaser(self.player.pos) for _ in range(settings.CHASER_COUNT)]
            self.time_left = settings.CHALLENGE_TIME
        else:
            self.chasers = []
            self.time_left = None

    def new_cookie(self, burnt=False):
        return Cookie(self.player.pos, self.player.radius, burnt)

    def update(self, dt):
        if self.result:
            return
        self.player.update(dt)

        for cookie in self.cookies[:]:
            if self.player.pos.distance_to(cookie.pos) < self.player.radius:
                self.cookies.remove(cookie)
                self.cookies.append(self.new_cookie(cookie.burnt))
                self.player.eat(cookie)
                if not cookie.burnt:
                    self.score += 1

        for chaser in self.chasers:
            chaser.update(dt, self.player.pos)
            if chaser.touches(self.player):
                self.result = "You got eaten!"

        if self.time_left is not None and not self.result:
            self.time_left = max(0.0, self.time_left - dt)
            if self.time_left == 0:
                self.result = "Time's up!"

    def draw(self, screen, fonts):
        screen.fill(settings.BG_COLOR)
        for cookie in self.cookies:
            cookie.draw(screen)
        self.player.draw(screen)
        for chaser in self.chasers:
            chaser.draw(screen)

        screen.blit(fonts["hud"].render(f"Cookies: {self.score}", True, settings.TEXT_COLOR), (16, 12))
        if self.time_left is not None:
            color = settings.HIGHLIGHT_COLOR if self.time_left < 5 else settings.TEXT_COLOR
            timer = fonts["hud"].render(f"Time: {self.time_left:4.1f}", True, color)
            screen.blit(timer, timer.get_rect(topright=(settings.WIDTH - 16, 12)))

        if self.result:
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
            overlay.fill(settings.OVERLAY_COLOR)
            screen.blit(overlay, (0, 0))
            draw_centered(screen, fonts["title"], self.result, settings.HEIGHT / 2 - 60)
            draw_centered(screen, fonts["hud"], f"Cookies eaten: {self.score}", settings.HEIGHT / 2 + 10)
            draw_centered(screen, fonts["small"], "Enter: play again    Esc: menu", settings.HEIGHT / 2 + 70)


def draw_centered(screen, font, text, y, color=settings.TEXT_COLOR):
    surface = font.render(text, True, color)
    screen.blit(surface, surface.get_rect(center=(settings.WIDTH / 2, y)))


def draw_menu(screen, fonts, selected):
    screen.fill(settings.BG_COLOR)
    draw_centered(screen, fonts["title"], settings.TITLE, 120)
    for i, (name, description) in enumerate(MODES):
        y = 250 + i * 90
        color = settings.HIGHLIGHT_COLOR if i == selected else settings.TEXT_COLOR
        marker = "> " if i == selected else ""
        draw_centered(screen, fonts["hud"], f"{marker}{i + 1}. {name}", y, color)
        draw_centered(screen, fonts["small"], description, y + 32)
    draw_centered(screen, fonts["small"], "Up/Down + Enter to choose    Esc: quit", settings.HEIGHT - 40)


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    fonts = {
        "title": pygame.font.Font(None, 72),
        "hud": pygame.font.Font(None, 40),
        "small": pygame.font.Font(None, 28),
    }

    selected = 0
    current = None  # the Round being played, or None while in the menu

    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type != pygame.KEYDOWN:
                continue
            elif current is None:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(MODES)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(MODES)
                elif event.key in (pygame.K_1, pygame.K_2):
                    selected = event.key - pygame.K_1
                    current = Round(MODES[selected][0])
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    current = Round(MODES[selected][0])
            elif event.key == pygame.K_ESCAPE:
                current = None
            elif current.result and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                current = Round(current.mode)

        if current is None:
            draw_menu(screen, fonts, selected)
        else:
            current.update(dt)
            current.draw(screen, fonts)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
