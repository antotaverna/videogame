import pygame

from videogame import settings


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, settings.PLAYER_SIZE, settings.PLAYER_SIZE)
        self.rect.center = (x, y)
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a]),
            (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w]),
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.pos += direction * settings.PLAYER_SPEED * dt
        self.pos.x = max(self.rect.width / 2, min(settings.WIDTH - self.rect.width / 2, self.pos.x))
        self.pos.y = max(self.rect.height / 2, min(settings.HEIGHT - self.rect.height / 2, self.pos.y))
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def draw(self, surface):
        pygame.draw.rect(surface, settings.PLAYER_COLOR, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption(settings.TITLE)
    clock = pygame.time.Clock()
    player = Player(settings.WIDTH / 2, settings.HEIGHT / 2)

    running = True
    while running:
        dt = clock.tick(settings.FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        player.update(dt)

        screen.fill(settings.BG_COLOR)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
