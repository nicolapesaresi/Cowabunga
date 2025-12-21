import pygame
from pathlib import Path
import cowabunga.env.settings as settings


class Button(pygame.sprite.Sprite):
    """Generic sprite for button.
    Args:
        width: width of the button.
        height: height of the button.
        x: x coord of top left corner.
        y: y coord of top left corner.
    """

    def __init__(self, width: int, height: int, x: int, y: int):
        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def clicked(self, click_pos: tuple[int, int]) -> bool:
        """Check that a click occurred inside the button.
        Args:
            click_pos: coords of the click (x, y).
        Returns
            (bool): whether the button has been clicked.
        """
        inside_x = self.x <= click_pos[0] <= self.x + self.width
        inside_y = self.y <= click_pos[1] <= self.y + self.height
        return inside_x and inside_y


class RoundButton(Button):
    """Generic sprite for round button.
    Args:
    size: height and width of the button.
    x: x coord of top left corner.
    y: y coord of top left corner.
    """

    def __init__(self, size: int, x: int, y: int):
        super().__init__(size, size, x, y)

    def clicked(self, click_pos: tuple[int, int]) -> bool:
        """Check that a click occurred inside the circle of the button, not just the rect.
        Args:
            click_pos: coords of the click (x, y).
        Returns
            (bool): whether the button has been clicked.
        """
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        dx = click_pos[0] - cx
        dy = click_pos[1] - cy
        return dx * dx + dy * dy <= (self.width / 2) ** 2


class LeaderboardButton(RoundButton):
    """Sprite for leaderboard button."""

    def __init__(self):
        """Instantiates leaderboard button."""
        size = settings.WIDTH * 0.1
        x = settings.WIDTH // 2 - size // 2 - size / 1.5
        y = settings.HEIGHT * 0.25 - size
        super().__init__(size, x, y)

        self.asset = Path(__file__).parent / ".." / "assets" / "leaderboard_icon.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for LeaderboardButton: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class InfoButton(RoundButton):
    """Sprite for info button."""

    def __init__(self):
        """Instantiates info button."""
        size = settings.WIDTH * 0.1
        x = settings.WIDTH // 2 - size // 2 + size / 1.5
        y = settings.HEIGHT * 0.25 - size
        super().__init__(size, x, y)

        self.asset = Path(__file__).parent / ".." / "assets" / "info_button.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for InfoButton: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class BackButton(RoundButton):
    """ "Go back button class."""

    def __init__(self):
        size = settings.WIDTH * 0.1
        x = settings.WIDTH // 2 - size // 2
        y = settings.HEIGHT * 0.25 - size
        super().__init__(size, x, y)

        self.asset = Path(__file__).parent / ".." / "assets" / "back_button.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for BackButton: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
