import pygame
import cowabunga.env.settings as settings


class TextSprite(pygame.sprite.Sprite):
    """Generic text sprite object."""

    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple[int, int, int],
        pos: tuple[int, int],
    ):
        super().__init__()
        self.font = font
        self.color = color
        self.text = text

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=pos)

    def update_text(self, new_text: str | int):
        """Updates sprite text."""
        if isinstance(new_text, int):
            new_text = str(new_text)
        self.text = new_text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


class LivesSprite(TextSprite):
    """Lives counter sprite."""

    def __init__(self, text: str | int):
        if isinstance(text, int):
            text = str(text)
        font = pygame.font.Font(None, size=settings.HEIGHT // 18)
        color = "white"
        pos = (2 * settings.WIDTH // 16, settings.WIDTH // 16)
        super().__init__(text, font, color, pos)
        self.rect.centerx = pos[0]


class ScoreSprite(TextSprite):
    """Lives counter sprite."""

    def __init__(self, text: str | int):
        if isinstance(text, int):
            text = str(text)
        font = pygame.font.Font(None, size=settings.HEIGHT // 18)
        color = "yellow"
        pos = (14 * settings.WIDTH // 16, settings.WIDTH // 16)
        super().__init__(text, font, color, pos)
        self.rect.centerx = pos[0]


class GameOverText(TextSprite):
    """Game over text sprite."""

    def __init__(self):
        text = "GAME OVER"
        font = pygame.font.Font(None, size=settings.HEIGHT // 6)
        color = "black"
        pos = (settings.WIDTH // 2, settings.HEIGHT // 3)
        super().__init__(text, font, color, pos)
        # center text
        self.rect.centerx = settings.WIDTH // 2


class FinalScoreSprite(TextSprite):
    """Final score sprite."""

    def __init__(self, text: str | int):
        if isinstance(text, int):
            text = str(text)
        font = pygame.font.Font(None, size=settings.HEIGHT // 7)
        color = "yellow"
        pos = (settings.WIDTH // 2, settings.HEIGHT // 2)
        super().__init__(text, font, color, pos)
        # center text
        self.rect.centerx = settings.WIDTH // 2
