import cowabunga.env.settings as settings
from cowabunga.env.objects.rect import Rect
from cowabunga.env.actions import Action

class Paddle(Rect):
    """Paddle object for CowabungaEnv."""
    def __init__(self, width = settings.WIDTH / 8, height = settings.HEIGHT / 30):
        """Initializes paddle object."""
        x = settings.WIDTH // 2 - width / 2
        y = settings.sea_level - height
        super().__init__(x, y, width, height)

    def move(self, direction: Action, pixels: int = settings.WIDTH / 80, margin: int = settings.WIDTH / 16):
        """Move the paddle based on key presses.
        
        Args:
            direction (str): Direction to move.
            pixels (int): Number of pixels to move.
            margin (int): Margin from the screen edge.
        """
        assert direction in (Action.LEFT, Action.RIGHT), f"Invalid movement direction for paddle: {direction}"
        if direction == Action.LEFT and self.x > margin:
            self.x -= pixels
        if direction == Action.RIGHT and self.x < settings.WIDTH - self.width - margin:
            self.x += pixels