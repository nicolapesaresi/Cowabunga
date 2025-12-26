import pygame
import cowabunga.env.settings as settings
from pathlib import Path


class SkySprite(pygame.sprite.Sprite):
    """Sprite for background sky."""

    def __init__(self):
        super().__init__()
        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.x = 0
        self.y = 0

        self.asset = Path(__file__).parent / ".." / "assets" / "sky.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for SkySprite: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("deepskyblue")
        self.rect = self.image.get_rect()
