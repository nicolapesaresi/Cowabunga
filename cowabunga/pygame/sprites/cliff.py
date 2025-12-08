import pygame
from cowabunga.env.objects.cliff import Cliff, RightCliff, LeftCliff
from cowabunga.utils.constants import GREEN

class CliffSprite(pygame.sprite.Sprite):
    """Sprite for cliff object."""
    def __init__(self, cliff: Cliff):
        super().__init__()
        self.cliff = cliff
        self.image = pygame.Surface((self.cliff.width, self.cliff.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(self.cliff.x, self.cliff.y))