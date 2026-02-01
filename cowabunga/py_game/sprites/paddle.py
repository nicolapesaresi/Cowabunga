from pathlib import Path

import pygame

from cowabunga.env import settings
from cowabunga.env.actions import Action
from cowabunga.env.objects.paddle import Paddle
from cowabunga.py_game.commands import CommandModes


class PaddleSprite(pygame.sprite.Sprite):
    """Sprite for paddle object."""

    def __init__(self, paddle: Paddle):
        super().__init__()
        self.paddle = paddle
        self.asset = Path(__file__).parent / ".." / "assets" / "paddle.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.paddle.width, self.paddle.height))
        except Exception as e:
            print(f"Unable to load image for PaddleSprite: {e}")
            self.image = pygame.Surface((self.paddle.width, self.paddle.height))
            self.image.fill("brown")
        self.rect = self.image.get_rect()

    def update(self):
        """Updates sprite with env info."""
        self.rect.x = self.paddle.x
        self.rect.y = self.paddle.y

    def get_key_input(self, commands: CommandModes) -> Action:
        """Get key input for paddle movement. Keyboard and click supported."""
        # keyboard/clicking mode
        if commands == CommandModes.CLICK:
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
        # drag mode
        elif commands == CommandModes.DRAG:
            # desktop mouse
            mouse_x, _ = pygame.mouse.get_pos()
            if mouse_x != 0:  # means there's a mouse
                half_width = self.paddle.width / 2
                target_x = max(half_width, min(mouse_x, settings.WIDTH - half_width))
                self.paddle.x = target_x - half_width
                return Action.NOOP_DRAG
            # touch screen
            for event in pygame.event.get():
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
                    pointer_x, _ = event.pos
                    half_width = self.paddle.width / 2
                    target_x = max(half_width, min(pointer_x, settings.WIDTH - half_width))
                    self.paddle.x = target_x - half_width
                    # no return as it already moves the paddle
            return Action.NOOP_DRAG
        else:
            raise ValueError(f"Invalid command mode {commands}")
