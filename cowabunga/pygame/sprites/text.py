import pygame
from cowabunga.utils.constants import WHITE, YELLOW, BLACK, WIDTH, HEIGHT

class TextSprite(pygame.sprite.Sprite):
    """Generic text sprite object."""
    def __init__(self, text: str, font: pygame.font.Font, color:tuple[int, int, int], pos: tuple[int, int]):
        super().__init__()
        self.font = font
        self.color = color
        self.text = text

        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=pos)

    def update_text(self, new_text: str|int):
        """Updates sprite text."""
        if isinstance(new_text, int):
            new_text = str(new_text)
        self.text = new_text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

class LivesSprite(TextSprite):
    """Lives counter sprite."""
    def __init__(self, text: str|int):
        if isinstance(text, int):
            text = str(text)
        font = pygame.font.Font(None, size = 40)
        color = WHITE
        pos = (50, 50)
        super().__init__(text, font, color, pos)

class ScoreSprite(TextSprite):
    """Lives counter sprite."""
    def __init__(self, text: str|int):
        if isinstance(text, int):
            text = str(text)
        font = pygame.font.Font(None, size = 40)
        color = YELLOW
        pos = (WIDTH - 50, 50)
        super().__init__(text, font, color, pos)

class GameOverText(TextSprite):
    """Game over text sprite."""
    def __init__(self):
        text = "GAME OVER"
        font = pygame.font.Font(None, size = 100)
        color = BLACK
        pos = (WIDTH // 2, 200)
        super().__init__(text, font, color, pos)
        # center text
        self.rect.centerx = WIDTH // 2

class FinalScoreSprite(TextSprite):
    """Final score sprite."""
    def __init__(self, text: str|int):
        if isinstance(text, int):
            text = str(text)
        font = pygame.font.Font(None, size = 80)
        color = YELLOW
        pos = (WIDTH // 2, 300)
        super().__init__(text, font, color, pos)
        # center text
        self.rect.centerx = WIDTH // 2