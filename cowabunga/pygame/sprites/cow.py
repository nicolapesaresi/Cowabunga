import pygame
from pygame.sprite import Group
from cowabunga.env.objects.cow import Cow

class CowSprite(pygame.sprite.Sprite):
    """Sprite for cow object."""
    def __init__(self, cow: Cow):
        super().__init__()
        self.cow = cow
        self.image = pygame.image.load("/Users/nicola/Desktop/vscode/Cowabunga/cowabunga/imgs/cow.jpg")
        self.image = pygame.transform.scale(self.image, (cow.width, cow.height))
        self.rect = self.image.get_rect(topleft=(self.cow.x, self.cow.y))

    def update(self):
        """Updates sprite with env info."""
        self.rect.x = self.cow.x
        self.rect.y = self.cow.y