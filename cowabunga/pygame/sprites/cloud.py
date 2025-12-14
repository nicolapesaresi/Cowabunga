import pygame
import random
import numpy as np
import cowabunga.env.settings as settings
from pathlib import Path


class CloudSprite(pygame.sprite.Sprite):
    """Sprite for background clouds."""

    def __init__(
        self,
        height: int = random.random() * settings.HEIGHT * 0.3 + settings.HEIGHT * 0.05,
        x: int | None = None,
        y: int = random.random() * settings.HEIGHT * 0.55 + settings.HEIGHT * 0.05,
        speed: int | None = None,
        alpha: int = 180,
    ):
        """Instantiates cloud sprite. If parameters are not specified, they are chosen randomly and starting position is just outside of the screen.
        Args:
            height: height of the cloud sprite.
            x: x position of the cloud sprite. If None, starts just outside of the left or right side of the screen.
            y: y position of the cloud sprite.
            speed: speed of the cloud sprite (pixels per update).
            alpha: transparency of the cloud sprite (0-255).
        """
        super().__init__()
        self.height = height
        self.width = self.height / settings.HEIGHT * settings.WIDTH
        if x:
            self.x = x
            speed_sign = 1
        else:
            self.x = random.choice([-self.width, settings.WIDTH])
            speed_sign = np.sign(self.x) * -1
        self.y = y
        self.alpha = alpha
        if speed:
            self.speed = speed
        else:
            self.speed = (
                random.random() * settings.WIDTH * 0.001 + settings.WIDTH * 0.0005
            ) * speed_sign

        # check cloud will enter screen if it starts outside
        if self.x < 0:
            assert (
                self.speed > 0
            ), f"Cloud with these x-coord and speed will never enter screen: {self.x, speed}"
        elif self.x >= settings.WIDTH:
            assert (
                self.speed < 0
            ), f"Cloud with these x-coord and speed will never enter screen: {self.x, speed}"

        self.asset = (
            Path(__file__).parent
            / ".."
            / "assets"
            / f"cloud_{random.choice((1,2,3))}.png"
        )
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for CloudSprite: {e}")
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill("gray")
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        """Updates cloud sprite according to its movement."""
        self.rect.x += self.speed
