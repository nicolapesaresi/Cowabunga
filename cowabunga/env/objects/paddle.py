from cowabunga.utils.constants import WIDTH, HEIGHT
from cowabunga.env.objects.rect import Rect
from cowabunga.env.actions import Action

class Paddle(Rect):
    """Paddle object for CowabungaEnv."""
    def __init__(self, width = 100, height = 20):
        """Initializes paddle object."""
        x = WIDTH // 2 - width / 2
        y = HEIGHT - 30
        super().__init__(x, y, width, height)

    def move(self, direction: Action, pixels: int = 5, margin: int = 50):
        """Move the paddle based on key presses.
        
        Args:
            direction (str): Direction to move.
            pixels (int): Number of pixels to move.
            margin (int): Margin from the screen edge.
        """
        assert direction in (Action.LEFT, Action.RIGHT), f"Invalid movement direction for paddle: {direction}"
        if direction == Action.LEFT and self.x > margin:
            self.x -= pixels
        if direction == Action.RIGHT and self.x < WIDTH - self.width - margin:
            self.x += pixels