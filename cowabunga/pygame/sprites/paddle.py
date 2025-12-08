import pygame
from cowabunga.env.objects.paddle import Paddle
from cowabunga.env.actions import Action
from cowabunga.utils.constants import BROWN

class PaddleSprite(pygame.sprite.Sprite):
    """Sprite for paddle object."""
    def __init__(self, paddle: Paddle):
        super().__init__()
        self.paddle = paddle
        self.image = pygame.Surface((self.paddle.width, self.paddle.height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()

    def update(self):
        """Updates sprite with env info."""
        self.rect.x = self.paddle.x
        self.rect.y = self.paddle.y

    def get_key_input(self):
        """Get key input for paddle movement."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move(Action.LEFT)
        if keys[pygame.K_RIGHT]:
            self.paddle.move(Action.RIGHT)
        self.update()