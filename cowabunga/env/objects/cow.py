from cowabunga.utils.constants import HEIGHT
from cowabunga.env.objects.rect import Rect

class Cow(Rect):
    """Cow object for CowabungaEnv."""
    def __init__(self):
        """Initializes cow object."""
        x = 0
        y = 120
        height = 50
        width = 50
        super().__init__(x, y, width, height)
        self.velocity = [1.3, 0]

    def move(self):
        """Moves cow based on it's velocity."""
        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def freefall(self, gravity = 0.1):
        """Makes cow fall to gravity."""
        self.velocity[1] += gravity

    def land(self):
        """Makes cow stop falling."""
        self.velocity[1] = 0

    def bounce(self):
        """Bounces cow off the paddle."""
        self.velocity[1] = -self.velocity[1]

    def check_fall_off(self, fall_y: int = HEIGHT - 30):
        if self.y > fall_y:
            return True
        else:
            return False