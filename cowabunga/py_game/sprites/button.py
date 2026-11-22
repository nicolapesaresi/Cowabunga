from pathlib import Path

import pygame

from cowabunga.env import settings


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

        Returns:
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

        Returns:
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
    """Go back button class."""

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


class CogsButton(RoundButton):
    """Cogs button to change commands."""

    def __init__(self, center: tuple[float, float] = (settings.WIDTH * 0.74, settings.HEIGHT * 0.37)):
        """Instantiates the cogs button.

        Args:
            center: (x, y) of the button center.
        """
        size = settings.WIDTH * 0.04
        super().__init__(size, center[0] - size / 2, center[1] - size / 2)

        self.asset = Path(__file__).parent / ".." / "assets" / "cogs_button.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for CogsButton: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class PauseButton(RoundButton):
    """Pause button class. By default big and centered; size and position can be given."""

    def __init__(self, size: float | None = None, x: float | None = None, y: float | None = None):
        size = size or settings.WIDTH * 0.1
        x = settings.WIDTH // 2 - size // 2 if x is None else x
        y = settings.HEIGHT // 2 - size if y is None else y
        super().__init__(size, x, y)

        self.asset = Path(__file__).parent / ".." / "assets" / "pause_icon.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for PauseButton: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class SoundButton(RoundButton):
    """Speaker button that opens the sound settings."""

    def __init__(self):
        size = settings.WIDTH * 0.05
        x = settings.WIDTH - size * 1.5
        y = size * 0.5
        super().__init__(size, x, y)

        self.asset = Path(__file__).parent / ".." / "assets" / "volume.png"
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Unable to load image for SoundButton: {e}")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill("red")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class TextButton(Button):
    """Rounded button with a text label."""

    def __init__(self, text: str, center: tuple[float, float]):
        """Instantiates the button.

        Args:
            text: button label.
            center: (x, y) of the button center.
        """
        font = pygame.font.Font(None, settings.HEIGHT // 18)
        label = font.render(text, True, "white")
        width = label.get_width() + settings.WIDTH * 0.04
        height = label.get_height() + settings.HEIGHT * 0.03
        super().__init__(width, height, center[0] - width / 2, center[1] - height / 2)

        self.image = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)
        shape = self.image.get_rect()
        pygame.draw.rect(self.image, (40, 25, 10, 200), shape, border_radius=shape.height // 2)
        pygame.draw.rect(self.image, (255, 215, 0), shape, width=3, border_radius=shape.height // 2)
        self.image.blit(label, label.get_rect(center=shape.center))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
