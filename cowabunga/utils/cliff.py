import pygame
from utils.constants import GREEN, WIDTH, HEIGHT

class Cliff(pygame.sprite.Sprite):
    """Class for cliff object."""
    def __init__(self, x, y, width=100, height=HEIGHT - 50):
        super().__init__()
        
        # self.image = pygame.image.load("imgs/cow.jpg")
        self.image = pygame.Surface((width, height))
        # self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


class LeftCliff(Cliff):
    """Class for left cliff object."""
    def __init__(self):
        self.topleft_corner = (0, 175)
        super().__init__(self.topleft_corner[0], self.topleft_corner[1])



class RightCliff(Cliff):
    """Class for right cliff object."""
    def __init__(self):
        self.topleft_corner = (WIDTH - 100, 175)
        super().__init__(self.topleft_corner[0], self.topleft_corner[1])