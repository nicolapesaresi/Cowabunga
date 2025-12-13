import pygame
import cowabunga.env.settings as settings
from pathlib import Path


class SeaSprite(pygame.sprite.Sprite):
    """Sprite for sea object.
    Args:
        x: x-coord of sprite's top left corner.
        y: y-coord of sprite's top left corner.
        width: width of sprite.
        height: height of sprite.
    """

    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.asset = Path(__file__).parent / ".." / "assets" / "sea.png"

    def wiggle(self):
        # to be implemented
        pass


class FrontSeaSprite(SeaSprite):
    """Sprite for front sea."""

    def __init__(self):
        color = "navy"
        width = settings.WIDTH * 1.5
        height = settings.HEIGHT // 10
        x = -settings.WIDTH * 0.1
        y = settings.sea_level - settings.HEIGHT * 0.01
        super().__init__(x, y, width, height)

        try:
            extra_height = settings.HEIGHT * 0.01
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(
                self.image, (self.width, self.height + extra_height)
            )
            self.rect = self.image.get_rect(topleft=(self.x, self.y - extra_height))
        except Exception as e:
            print(f"Unable to load image for SeaSprite: {e}")
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(color)
            self.image.set_alpha(180)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))


class BackSeaSprite(SeaSprite):
    """Sprite for back sea."""

    def __init__(self):
        color = "blue"
        width = settings.WIDTH * 1.5
        height = settings.HEIGHT // 10
        offset = width / 20  # offset from front sea
        x = -settings.WIDTH * 0.1 + offset
        y = settings.sea_level - settings.HEIGHT * 0.02
        super().__init__(x, y, width, height)

        try:
            extra_height = settings.HEIGHT * 0.03
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(
                self.image, (self.width, self.height + extra_height)
            )
            self.rect = self.image.get_rect(topleft=(self.x, self.y - extra_height))
        except Exception as e:
            print(f"Unable to load image for SeaSprite: {e}")
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(color)
            self.image.set_alpha(180)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
