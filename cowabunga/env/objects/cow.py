from cowabunga.utils.constants import HEIGHT, WIDTH
from cowabunga.env.objects.rect import Rect

class Cow(Rect):
    """Cow object for CowabungaEnv."""
    def __init__(self):
        """Initializes cow object."""
        x = 0
        y = 125
        height = 50
        width = 50
        super().__init__(x, y, width, height)
        self.velocity = [1.25, 0]

    def move(self):
        """Moves cow based on it's velocity."""
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def freefall(self, gravity = 0.15):
        """Makes cow fall to gravity."""
        self.velocity[1] += gravity

    def land(self, landing_y: int):
        """Makes cow stop falling.
        Args:
            landing_y: y coord of landing, to avoid rounding errors.
        """
        self.velocity[1] = 0
        self.y = landing_y - self.height

    def bounce(self, bounce_y: int):
        """Bounces cow off the paddle.
        Args:
            bounce_y: y coord of landing spot, to start the bounce from. Avoids rounding errors.
        """
        self.velocity[1] = -self.velocity[1]
        self.y = bounce_y - self.height

    def is_dead(self, fall_y: int = HEIGHT):
        """Checks if cow has fallen off the screen.
        Args:
            fall_y: y coord value that defines when a cow has fallen off.
        """
        if self.y > fall_y:
            return True
        else:
            return False
        
    def is_safe(self, safe_x: int = WIDTH):
        """Checks if cow has safely crossed.
        Args:
            safe_x: x coord value that defines when a cow has safely crossed.
        """
        if self.x > safe_x:
            return True
        else:
            return False