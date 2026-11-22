import random
from pathlib import Path

import pygame

from cowabunga.env import settings

ASSETS_DIR = Path(__file__).parent / ".." / "assets"
CLOUD_ASSETS = ("cloud_1.png", "cloud_2.png", "cloud_3.png")


class CloudSprite(pygame.sprite.Sprite):
    """Sprite for background clouds.

    Each cloud has a depth in [0, 1] (0 = far, 1 = near) that sets its size, speed, height in the sky
    and transparency, so that far clouds are small, slow and faint (parallax effect).
    """

    _base_images: list[pygame.Surface] | None = None

    @classmethod
    def base_images(cls) -> list[pygame.Surface]:
        """Loads cloud images once and caches them for all clouds."""
        if cls._base_images is None:
            cls._base_images = []
            for name in CLOUD_ASSETS:
                try:
                    cls._base_images.append(pygame.image.load(ASSETS_DIR / name))
                except Exception as e:
                    print(f"Unable to load image for CloudSprite: {e}")
        return cls._base_images

    def __init__(
        self,
        depth: float | None = None,
        height: float | None = None,
        x: float | None = None,
        y: float | None = None,
        speed: float | None = None,
        alpha: int | None = None,
    ):
        """Instantiates cloud sprite. Parameters that are not specified are derived from depth,
            and starting position is just outside the right edge of the screen.

        Args:
            depth: distance of the cloud, 0 (far) to 1 (near). By default random.
            height: height of the cloud sprite.
            x: x position of the cloud sprite. By default just outside the right edge.
            y: y position of the cloud sprite. By default a random y coord, higher for far clouds.
            speed: speed of the cloud sprite (pixels per update).
            alpha: transparency of the cloud sprite (0-255).
        """
        super().__init__()
        if depth is None:
            depth = random.random()
        self.depth = depth
        if height is None:
            height = settings.HEIGHT * (0.10 + 0.15 * depth) * random.uniform(0.9, 1.1)
        self.height = height
        self.width = self.height / settings.HEIGHT * settings.WIDTH
        if x is None:
            x = settings.WIDTH
        if y is None:
            # far clouds sit higher in the sky, near ones can go lower
            y = settings.HEIGHT * (0.01 + random.random() * (0.15 + 0.25 * depth))
        if speed is None:
            speed = -(0.4 + 1.2 * depth) * random.uniform(0.9, 1.1) * settings.WIDTH / 1600
        if alpha is None:
            alpha = int(150 + 105 * depth)  # near clouds opaque, far ones fade into the sky
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.alpha = alpha

        # check cloud will enter screen if it starts outside
        if self.x < 0:
            assert self.speed > 0, f"Cloud with these x-coord and speed will never enter screen: {self.x, speed}"
        elif self.x >= settings.WIDTH:
            assert self.speed < 0, f"Cloud with these x-coord and speed will never enter screen: {self.x, speed}"

        size = (round(self.width), round(self.height))
        images = self.base_images()
        if images:
            self.image = pygame.transform.smoothscale(random.choice(images), size)
            if random.random() < 0.5:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill("gray")
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(topleft=(round(self.x), round(self.y)))

    def is_offscreen(self) -> bool:
        """True once the cloud has fully left the screen in its direction of movement."""
        return (self.x > settings.WIDTH and self.speed >= 0) or (self.x + self.width < 0 and self.speed <= 0)

    def update(self):
        """Updates cloud sprite according to its movement."""
        # position is kept as float so slow clouds move smoothly (rect only stores ints)
        self.x += self.speed
        self.rect.x = round(self.x)
