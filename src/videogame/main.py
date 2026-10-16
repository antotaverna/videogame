import math
import random

import pygame

from videogame import settings


def random_chips(radius, count):
    """Chip offsets (relative to the cookie center) scattered inside the cookie."""
    chips = []
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, radius * 0.7)
        chips.append(pygame.Vector2(math.cos(angle), math.sin(angle)) * dist / radius)
    return chips


def draw_cookie(surface, center, radius, chips):
    pygame.draw.circle(surface, settings.EDGE_COLOR, center, radius)
    pygame.draw.circle(surface, settings.DOUGH_COLOR, center, radius * 0.88)
    chip_radius = max(2, radius * 0.12)
    for offset in chips:
        pygame.draw.circle(surface, settings.CHIP_COLOR, center + offset * radius, chip_radius)


class Cookie:
    def __init__(self, avoid_pos, avoid_radius):
        self.radius = settings.COOKIE_RADIUS
        self.chips = random_chips(self.radius, 3)
        margin = self.radius + 10
        # Don't spawn right on top of the player.
        while True:
            self.pos = pygame.Vector2(
                random.uniform(margin, settings.WIDTH - margin),
                random.uniform(margin, settings.HEIGHT - margin),
            )
            if self.pos.distance_to(avoid_pos) > avoid_radius + self.radius + 40:
                break

    def draw(self, surface):
        draw_cookie(surface, self.pos, self.radius, self.chips)


class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.radius = settings.PLAYER_RADIUS
        # Chips around the rim so they don't clutter the face.
        self.chips = [
            pygame.Vector2(math.cos(a), math.sin(a)) * 0.72
            for a in (i * 2 * math.pi / 7 + 0.3 for i in range(7))
        ]
        self.facing = pygame.Vector2(1, 0)
        self.chomp_timer = 0.0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w]),
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
            self.facing = direction
        self.pos += direction * settings.PLAYER_SPEED * dt
        self.pos.x = max(self.radius, min(settings.WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(settings.HEIGHT - self.radius, self.pos.y))
        self.chomp_timer = max(0.0, self.chomp_timer - dt)

    def eat(self):
        self.radius = min(settings.PLAYER_MAX_RADIUS, self.radius + settings.PLAYER_GROWTH)
        self.chomp_timer = 0.15

    def draw(self, surface):
        draw_cookie(surface, self.pos, self.radius, self.chips)

        # The face looks at the viewer and shifts slightly toward the movement direction.
        r = self.radius
        look = self.facing * r * 0.15
        for s in (-1, 1):
            eye = self.pos + pygame.Vector2(s * r * 0.32, -r * 0.22) + look
            pygame.draw.circle(surface, (255, 255, 255), eye, r * 0.18)
            pygame.draw.circle(surface, (0, 0, 0), eye + self.facing * r * 0.07, r * 0.09)

        # Mouth: wide open right after a bite, otherwise a smile.
        mouth_center = self.pos + pygame.Vector2(0, r * 0.32) + look
        if self.chomp_timer > 0:
            pygame.draw.circle(surface, (80, 20, 20), mouth_center, r * 0.3)
        else:
            smile = pygame.Rect(0, 0, r * 0.7, r * 0.45)
            smile.center = (round(mouth_center.x), round(mouth_center.y - r * 0.12))
            pygame.draw.arc(surface, (80, 20, 20), smile, math.pi * 1.1, math.pi * 1.9, max(3, round(r * 0.11)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    player = Player(settings.WIDTH / 2, settings.HEIGHT / 2)
    cookies = [Cookie(player.pos, player.radius) for _ in range(settings.COOKIE_COUNT)]
    score = 0

    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        player.update(dt)

        for cookie in cookies[:]:
            if player.pos.distance_to(cookie.pos) < player.radius:
                cookies.remove(cookie)
                cookies.append(Cookie(player.pos, player.radius))
                player.eat()
                score += 1

        screen.fill(settings.BG_COLOR)
        for cookie in cookies:
            cookie.draw(screen)
        player.draw(screen)
        screen.blit(font.render(f"Cookies: {score}", True, settings.TEXT_COLOR), (16, 12))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
