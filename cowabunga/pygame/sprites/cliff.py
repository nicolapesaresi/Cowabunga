import pygame
import cowabunga.env.settings as settings
from cowabunga.env.objects.cliff import Cliff, RightCliff, LeftCliff
from pathlib import Path


class CliffSprite(pygame.sprite.Sprite):
    """Sprite for cliff object."""

    def __init__(self, cliff: Cliff):
        super().__init__()
        self.cliff = cliff
        try:
            if isinstance(self.cliff, LeftCliff):
                self.asset = Path(__file__).parent / ".." / "assets" / "leftcliff.png"
                extra_height = settings.HEIGHT / 12
                extra_width = settings.WIDTH / 22
                self.image = pygame.image.load(self.asset)
                self.image = pygame.transform.scale(
                    self.image,
                    (self.cliff.width + extra_width, self.cliff.height + extra_height),
                )
                self.rect = self.image.get_rect(
                    topleft=(self.cliff.x, self.cliff.y - extra_height)
                )
            elif isinstance(self.cliff, RightCliff):
                self.asset = Path(__file__).parent / ".." / "assets" / "rightcliff.png"
                extra_height = settings.HEIGHT / 12
                extra_width = settings.WIDTH / 25
                self.image = pygame.image.load(self.asset)
                self.image = pygame.transform.scale(
                    self.image,
                    (self.cliff.width + extra_width, self.cliff.height + extra_height),
                )
                self.rect = self.image.get_rect(
                    topleft=(self.cliff.x - extra_width, self.cliff.y - extra_height)
                )
            else:
                raise ValueError("Unknown cliff type")
        except Exception as e:
            print(f"Unable to load image for CliffSprite: {e}")
            self.image = pygame.Surface((self.cliff.width, self.cliff.height))
            self.image.fill("green")
            self.rect = self.image.get_rect(
                topleft=(self.cliff.x, self.cliff.y - extra_height)
            )
