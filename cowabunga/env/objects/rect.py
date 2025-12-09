class Rect:
    """Generic class for game element rect."""
    def __init__(self, x: int, y: int, width: int, height: int):
        """Initializes game element rectangle.
        Args:
            x: x-coord of top left corner.
            y: y-coord of top left corner.
            width: width of the rectangle.
            height: height of the rectangle.
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def get_hitbox(self) -> tuple[int, int, int, int]:
        """Calculates hitbox coordinates
        Returns:
            hitbox: tuple of (x1, y1, x2, x2) coordinates, where (x1,y1) is top left corner and (x2,y2) is bottom right corner.
        """
        x1 = self.x
        y1 = self.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        return x1, y1, x2, y2
    
    def check_collision(self, other_hitbox:tuple[int]) -> bool:
        """Checks collision with another rect hitbox.
        Args:
            other_hitbox: (x1, y1, x2, y2) of other hitbox
        Returns:
            (bool): whether collision happened or not
        """
        x1, y1, x2, y2 = self.get_hitbox()
        ox1, oy1, ox2, oy2 = other_hitbox

        # AABB collision check
        return not (
            x2 < ox1 or   # self is left of other
            x1 > ox2 or   # self is right of other
            y2 < oy1 or   # self is above other
            y1 > oy2      # self is below other
        )
    
    def check_landing_collision(self, ground_hitbox:tuple[int]) -> bool:
        """Checks collision of bottom with the ground, meaning it ground has to be below object.
        Args:
            ground_hitbox: (x1, y1, x2, y2) of ground hitbox.
        Returns:
            (bool): whether collision with the ground (below) has happened.
        """
        assert(hasattr(self, "velocity")), f"instance of Rect has no attribute self.velocity, needed to check collision with ground."
        rect_bottom = self.y + self.width
        previous_bottom = self.y + self.width - self.velocity[1]
        return self.check_collision(ground_hitbox) and previous_bottom <= ground_hitbox[1] <= rect_bottom