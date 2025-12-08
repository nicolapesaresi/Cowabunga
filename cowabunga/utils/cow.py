import pygame

from utils.constants import HEIGHT
from utils.paddle import Paddle
from pygame.sprite import Group

class Cow(pygame.sprite.Sprite):
    """Class for cow object."""
    def __init__(self):
        super().__init__()

        # initial position
        self.starting_x = 0
        self.starting_y = 120

        self.image = pygame.image.load("imgs/cow.jpg")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(self.starting_x, self.starting_y))
        # intial velocity
        self.velocity = [1.3, 0]  # X and Y speed


    def update(self):
        """Update cow's position."""

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def freefall(self, gravity = 0.1):
        """Make cow fall to gravity."""
        self.velocity[1] += gravity

    def bounce(self):
        """Bounce cow off the paddle."""
        self.velocity[1] = -self.velocity[1] 

    def handle_paddle_collision(self, paddle: Paddle):
        """Detect collision with paddle."""
        if pygame.sprite.collide_mask(self, paddle):
            self.bounce()

    def handle_cliff_collision(self, cliff_group: Group):
        """Detect collision with cliffs."""
        collisions = pygame.sprite.spritecollide(self, cliff_group, False)
        if len(collisions) == 0:
            self.freefall()
        else:
            for cliff in collisions:
                if self.rect.bottom <= cliff.rect.top:    
                    self.velocity[1] = 0
    
    
    def check_fall_off(self, fall_y: int = HEIGHT - 30):
        if self.rect.y > fall_y:
            self.kill()
            return True
        else:
            return False

