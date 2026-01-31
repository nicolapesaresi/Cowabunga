import pygame
from cowabunga.env.objects.paddle import Paddle
from cowabunga.env.actions import Action
from pathlib import Path


class PaddleSprite(pygame.sprite.Sprite):
    """Sprite for paddle object."""

    def __init__(self, paddle: Paddle):
        super().__init__()
        self.paddle = paddle
        self.asset = Path(__file__).parent / ".." / "assets" / "paddle.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(
                self.image, (self.paddle.width, self.paddle.height)
            )
        except Exception as e:
            print(f"Unable to load image for PaddleSprite: {e}")
            self.image = pygame.Surface((self.paddle.width, self.paddle.height))
            self.image.fill("brown")
        self.rect = self.image.get_rect()

    def update(self):
        """Updates sprite with env info."""
        self.rect.x = self.paddle.x
        self.rect.y = self.paddle.y

    def get_key_input(self) -> Action:
        """Get key input for paddle movement. Keyboard and click supported."""
        # keyboard input (priority)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            return Action.LEFT
        elif keys[pygame.K_RIGHT]:
            return Action.RIGHT

        # mouse input
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # left mouse button
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x < self.paddle.x + (self.paddle.width // 2):
                return Action.LEFT
            else:
                return Action.RIGHT

        return Action.NOOP
