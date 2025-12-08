import pygame

from utils.constants import WIDTH, HEIGHT, BROWN

class Paddle(pygame.sprite.Sprite):
    """Class for paddle object."""
    def __init__(self, width=100, height=20):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()

        #initial position
        self.rect.x = WIDTH // 2 - 50
        self.rect.y = HEIGHT - 30

    def move(self, direction: str, pixels: int = 5, margin: int = 50):
        """Move the paddle based on key presses.
        
        Args:
            direction (str): Direction to move ('left' or 'right').
            pixels (int): Number of pixels to move.
            margin (int): Margin from the screen edge.
        """

        if direction == "left" and self.rect.x > margin:
            self.rect.x -= pixels
        if direction == "right" and self.rect.x < WIDTH - self.rect.width - margin:
            self.rect.x += pixels

    def get_key_input(self):
        """Get key input for paddle movement."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move("left")
        if keys[pygame.K_RIGHT]:
            self.move("right")