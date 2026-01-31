import cowabunga.env.settings as settings
from cowabunga.env.objects.rect import Rect
from cowabunga.env.actions import Action


class Paddle(Rect):
    """Paddle object for CowabungaEnv."""

    def __init__(self, width=settings.WIDTH / 8, height=settings.HEIGHT / 15):
        """Initializes paddle object."""
        x = settings.WIDTH // 2 - width / 2
        y = settings.sea_level - height
        super().__init__(x, y, width, height)

        self.landing_spots = [
            settings.spot_0 - self.width // 2,
            settings.spot_1 - self.width // 2,
            settings.spot_2 - self.width // 2,
            settings.spot_3 - self.width // 2,
            settings.spot_4 - self.width // 2,
        ]
        self.current_spot = len(self.landing_spots) // 2  # middle spot
        self.step_movement = (
            self.landing_spots[1] - self.landing_spots[0]
        ) / settings.ACTION_COOLDOWN
        # this assumes equidistant landing spots

    def move(
        self,
        direction: Action,
    ):
        """Move the paddle based on key presses.

        Args:
            direction (str): Direction to move.
        """
        assert direction in (
            Action.LEFT,
            Action.RIGHT,
        ), f"Invalid movement direction for paddle: {direction}"
        if direction == Action.LEFT and self.current_spot > 0:
            self.current_spot -= 1
        elif (
            direction == Action.RIGHT
            and self.current_spot < len(self.landing_spots) - 1
        ):
            self.current_spot += 1

    def animate_move(self):
        """Performs a little movement in the action direction, to animate fluently."""
        target_x = self.landing_spots[self.current_spot]
        delta = target_x - self.x
        if abs(delta) <= self.step_movement:
            self.x = target_x
        else:
            self.x += self.step_movement * (1 if delta > 0 else -1)
