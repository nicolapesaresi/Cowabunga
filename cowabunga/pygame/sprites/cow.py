import pygame
import random
from cowabunga.env.objects.cow import Cow
from pathlib import Path
from dataclasses import dataclass


@dataclass
class CowType:
    """Contains probability of appearing and path to asset of a type of cow."""

    prob: float
    asset: str


class CowSprite(pygame.sprite.Sprite):
    """Sprite for cow object."""

    COW_TYPES = {
        "default": CowType(0.6, "cow.png"),
        "brown": CowType(0.3, "cow_brown.png"),
        "highlands": CowType(0.1, "cow_highlands.png"),
    }

    def __init__(self, cow: Cow, cow_type: str | None = None):
        super().__init__()
        self.cow = cow
        self.load_asset(cow_type)
        self.rect = self.image.get_rect(topleft=(self.cow.x, self.cow.y))

    def update(self):
        """Updates sprite with env info."""
        self.rect.x = self.cow.x
        self.rect.y = self.cow.y

    @classmethod
    def random_type(cls) -> CowType:
        """Select a cow type based on probability weights."""
        names = list(cls.COW_TYPES.keys())
        weights = [cls.COW_TYPES[name].prob for name in names]
        chosen_name = random.choices(names, weights=weights, k=1)[0]
        return cls.COW_TYPES[chosen_name]

    def load_asset(self, cow_type: str):
        """Loads asset depending on cow type, randomly if not specified.
        Args:
            cow_type: one of the keys of self.COW_TYPES or None. In this case, chosen randomly accordingly to probs.
        """
        if cow_type and cow_type in self.COW_TYPES:
            self.cow_type = self.COW_TYPES[cow_type]
        else:
            self.cow_type = self.random_type()
        self.asset = Path(__file__).parent / ".." / "assets" / self.cow_type.asset
        try:
            self.image = pygame.image.load(self.asset)
            self.image = pygame.transform.scale(
                self.image, (self.cow.width, self.cow.height)
            )
        except Exception as e:
            print(f"Unable to load image for CowSprite: {e}")
            self.image = pygame.Surface(
                (self.cow.width, self.cow.height), pygame.SRCALPHA
            )
            self.image.fill("white")
