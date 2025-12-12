import pygame
import cowabunga.env.settings as settings

class SeaSprite(pygame.sprite.Sprite):
    """Sprite for sea object.
    Args:
        x: x-coord of sprite's top left corner.
        y: y-coord of sprite's top left corner.
        width: width of sprite.
        height: height of sprite.
        color: color of sprite.
    """
    def __init__(self, x: int, y:int, width:int, height:int, color: str|tuple[int]):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.image.set_alpha(180)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def wiggle(self):
        #to be implemented
        pass

class FrontSeaSprite(SeaSprite):
    """Sprite for front sea."""
    def __init__(self):
        color = "navy"
        width = settings.WIDTH * 1.5
        height = settings.HEIGHT // 4
        x = - settings.WIDTH * 0.1
        y = settings.sea_level - settings.HEIGHT * 0.01
        super().__init__(x, y, width, height, color)

class BackSeaSprite(SeaSprite):
    """Sprite for back sea."""
    def __init__(self):
        color = "blue"
        width = settings.WIDTH * 1.5
        height = settings.HEIGHT // 4
        x = - settings.WIDTH * 0.1
        y = settings.sea_level - settings.HEIGHT * 0.02
        super().__init__(x, y, width, height, color)