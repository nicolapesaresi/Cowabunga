import pygame
import random
import cowabunga.env.settings as settings
from pathlib import Path


class CloudSprite(pygame.sprite.Sprite):
    """Sprite for background clouds."""

    def __init__(
        self,
        height: int | None = None,
        x: int | None = None,
        y: int | None = None,
        speed: float | None = None,
        alpha: int = 180,
    ):
        """Instantiates cloud sprite. If parameters are not specified, they are chosen randomly and starting position is just outside of the screen.
        Args:
            height: height of the cloud sprite.
            x: x position of the cloud sprite. By default a random x coord.
            y: y position of the cloud sprite. By default a random y coord.
            speed: speed of the cloud sprite (pixels per update).
            alpha: transparency of the cloud sprite (0-255).
        """
        super().__init__()
        if height is None:
            height = random.random() * settings.HEIGHT * 0.2 + settings.HEIGHT * 0.1
        if x is None:
            x = random.random() * settings.WIDTH
        if y is None:
            y = random.random() * settings.HEIGHT * 0.40 + settings.HEIGHT * 0.01
        if speed is None:
            speed = -(
                random.random() * settings.WIDTH * 0.0005 + settings.WIDTH * 0.0005
            )
        self.height = height
        self.width = self.height / settings.HEIGHT * settings.WIDTH
        self.x = x
        self.y = y
        self.speed = speed
        self.alpha = alpha

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
