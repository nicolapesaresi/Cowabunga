import pygame
from pathlib import Path
import cowabunga.env.settings as settings


class SeaSprite(pygame.sprite.Sprite):
    """Generic sprite for sea layers."""

    def __init__(
        self,
        *,
        x: float,
        y: float,
        width: int,
        height: int,
        speed: float,
        color: str,
        alpha: int,
        extra_height: int = 0,
    ):
        """Instantiates SeaSprite object.
        Args:
            x: initial x coord.
            y: initial y coord.
            width: width of the sea layer.
            height: height of the sea layer.
            speed: horizontal scrolling speed.
            color: fallback color if image loading fails.
            alpha: transparency level (0-255) if image loading fails.
            extra_height: extra height to add to the sea sprite for overlap.
        """
        super().__init__()

        self.y = y
        self.speed = speed
        self.asset = Path(__file__).parent / ".." / "assets" / "sea.png"
        self.image = self._load_image(width, height + extra_height, color, alpha)
        self.rect = self.image.get_rect(topleft=(x, y - extra_height))

        # tiling / scrolling
        self.tile_width = self.rect.width
        self.offset_x = 0
        self.num_tiles = settings.WIDTH // self.tile_width + 2

    def _load_image(self, width, height, color, alpha):
        """Load sea image or fallback to colored surface."""
        try:
            image = pygame.image.load(self.asset)
            return pygame.transform.scale(image, (width, height))
        except Exception:
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill(color)
            surface.set_alpha(alpha)
            return surface

    def update(self):
        self.offset_x = (self.offset_x + self.speed) % self.tile_width

    def draw(self, screen: pygame.Surface):
        for i in range(self.num_tiles):
            x = (i - 1) * self.tile_width + self.offset_x
            screen.blit(self.image, (x, self.rect.y))


class FrontSeaSprite(SeaSprite):
    """Sprite for front sea."""

    def __init__(self):
        super().__init__(
            x=-settings.WIDTH * 0.1,
            y=settings.sea_level - settings.HEIGHT * 0.01,
            width=int(settings.WIDTH * 1.5),
            height=settings.HEIGHT // 10,
            speed=settings.WIDTH / 1000,
            color="navy",
            alpha=180,
            extra_height=int(settings.HEIGHT * 0.01),
        )


class BackSeaSprite(SeaSprite):
    """Sprite for back sea."""

    def __init__(self):
        super().__init__(
            x=-settings.WIDTH * 0.1 + settings.WIDTH / 20,
            y=settings.sea_level - settings.HEIGHT * 0.02,
            width=int(settings.WIDTH * 1.5),
            height=settings.HEIGHT // 10,
            speed=settings.WIDTH / 1500,
            color="blue",
            alpha=255,
            extra_height=int(settings.HEIGHT * 0.03),
        )
