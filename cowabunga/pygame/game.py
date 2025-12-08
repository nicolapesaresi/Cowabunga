import pygame
import random
from pygame.sprite import Group
from cowabunga.utils.utils import create_sprite
from cowabunga.utils.constants import WIDTH, HEIGHT, FPS, WHITE, BLUE, BROWN, LIGHT_BLUE, GREEN
from cowabunga.env.env import CowabungaEnv
from cowabunga.pygame.sprites.cow import CowSprite
from cowabunga.pygame.sprites.cliff import CliffSprite
from cowabunga.pygame.sprites.paddle import PaddleSprite


class PygameRenderer():
    """Pygame renderer for CowabungaEnv."""
    def __init__(self, seed: int|None = None):
        """Initializes pygame renderer.
        Args:
            seed: seed to be passed to the env for random cow generation.
        """
        self.seed = seed
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cowabunga - Pygame Edition")
        self.main_menu()

    def main_menu(self):
        """Renders main menu of the game."""
        # TODO: implement
        self.env = CowabungaEnv(self.seed)
        self.run()

    def load_gamescreen(self):
        """Loads main game elements, paddle and cliffs groups."""
        self.paddle = PaddleSprite(self.env.paddle)
        self.player = Group()
        self.player.add(self.paddle)
        self.cliffs = Group()
        for cliff in self.env.cliffs:
            self.cliffs.add(CliffSprite(cliff))

    def run(self):
        """Runs env loop in pygame."""
        clock = pygame.time.Clock()
        self.load_gamescreen()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Player input
            self.paddle.get_key_input()
            self.env.step(0)  # FIX HERE!!!
            # Cow logic
            self.update_cows()

            # Draw elements
            self.screen.fill(LIGHT_BLUE)
            self.cliffs.draw(self.screen)
            self.cows.draw(self.screen)
            self.player.draw(self.screen)
            
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()

    def update_cows(self):
        """Updates cow group using env info."""
        self.cows = Group()
        for cow in self.env.cows:
            self.cows.add(CowSprite(cow))