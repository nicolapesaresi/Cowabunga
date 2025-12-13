import cowabunga.env.settings as settings
from cowabunga.env.objects.rect import Rect


class Cliff(Rect):
    """Cliff object for CowabungaEnv."""

    def __init__(self, x, y, width=settings.WIDTH / 8, height=settings.HEIGHT * 1.1):
        super().__init__(x, y, width, height)


class LeftCliff(Cliff):
    """Class for left cliff object."""

    def __init__(self):
        self.topleft_corner = (
            0,
            settings.left_cliff_height,
        )  # defined there to be used by Cow for starting y
        super().__init__(self.topleft_corner[0], self.topleft_corner[1])


class RightCliff(Cliff):
    """Class for right cliff object."""

    def __init__(self):
        self.topleft_corner = (
            settings.WIDTH - settings.WIDTH / 8,
            settings.HEIGHT / 2.4,
        )
        super().__init__(self.topleft_corner[0], self.topleft_corner[1])
