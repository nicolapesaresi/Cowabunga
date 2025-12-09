from cowabunga.utils.constants import WIDTH, HEIGHT
from cowabunga.env.objects.rect import Rect

class Cliff(Rect):
    """Cliff object for CowabungaEnv."""
    def __init__(self, x, y, width=100, height=HEIGHT - 50):
        super().__init__(x, y, width, height)

class LeftCliff(Cliff):
    """Class for left cliff object."""
    def __init__(self):
        self.topleft_corner = (0, 175)
        super().__init__(self.topleft_corner[0], self.topleft_corner[1])

class RightCliff(Cliff):
    """Class for right cliff object."""
    def __init__(self):
        self.topleft_corner = (WIDTH - 100, 250)
        super().__init__(self.topleft_corner[0], self.topleft_corner[1])