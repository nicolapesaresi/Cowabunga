import pygame
import cowabunga.env.settings as settings
from cowabunga.pygame.sprites.text import TextSprite


class InfoPage:
    """Page displaying instructions and credits."""

    def __init__(self):
        """Instantiates InfoPage class."""
        # lines are tuples (text, style)
        self.lines = [
            ("Commands", "header"),
            ("Left arrow / Right arrow - move paddle", "text"),
            ("Spacebar - pause game", "text"),
            ("Credits", "header"),
            ("Original game and idea by Mark Andrade - AndradeArts", "text"),
            ("Pygame version created by Nicola Pesaresi", "text"),
        ]

        self.sprites = pygame.sprite.Group()
        color = {"header": "yellow", "text": "white"}
        font_size = {"header": settings.HEIGHT // 15, "text": settings.HEIGHT // 25}
        start_y = int(settings.HEIGHT * 0.3)
        spacing = font_size["text"] * 1.75

        for i, (text, style) in enumerate(self.lines):
            y = start_y + i * spacing
            sprite = TextSprite(
                text=text,
                font=pygame.font.Font(None, font_size[style]),
                color=color[style],
                pos=(settings.WIDTH // 2, y),
            )
            sprite.rect.centerx = settings.WIDTH // 2
            self.sprites.add(sprite)

    def draw(self, screen: pygame.Surface):
        """Draw all lines centered.
        Args:
            screen: pygame surface to draw on.
        """
        self.sprites.draw(screen)
