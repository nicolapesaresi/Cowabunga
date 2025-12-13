import pygame
import random
import cowabunga.env.settings as settings
from pygame.sprite import Group
from cowabunga.env.env import CowabungaEnv
from cowabunga.env.objects.cow import Cow
from cowabunga.pygame.sprites.cow import CowSprite
from cowabunga.pygame.sprites.cliff import CliffSprite
from cowabunga.pygame.sprites.paddle import PaddleSprite
from cowabunga.pygame.sprites.sea import FrontSeaSprite, BackSeaSprite
from cowabunga.pygame.sprites.sky import SkySprite
from cowabunga.pygame.sprites.text import LivesSprite, ScoreSprite, GameOverText, FinalScoreSprite

class PygameRenderer():
    """Pygame renderer for CowabungaEnv."""
    def __init__(self, seed: int|None = None):
        """Initializes pygame renderer.
        Args:
            seed: seed to be passed to the env for random cow generation.
        """
        self.seed = seed
        self.fps = settings.FPS

        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
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
        self.cow_sprites : dict[int, Cow]= {}
        self.cows = Group()
        self.update_cows()
        # aestethics
        self.sky = SkySprite()
        self.back_sea = BackSeaSprite()
        self.front_sea = FrontSeaSprite()
        # score and lives
        self.lives = LivesSprite(self.env.lives)
        self.score = ScoreSprite(self.env.score)
        self.texts = Group()
        self.texts.add(self.lives, self.score)

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
            self.env.step(0)  # TODO: this only supports human player actions, change to support Agent
            # Cow logic
            self.update_cows()
            # Drawing
            self.draw_screen()
            self.draw_text()
            pygame.display.flip()

            clock.tick(self.fps)
            if self.env.done:
                running = False
                self.gameover_screen()
        self.close()

    def update_cows(self):
        """Updates cow group using env info."""
        current_cow_ids = {cow.id for cow in self.env.cows}
        # Remove sprites for deleted cows
        for cow_id, sprite in list(self.cow_sprites.items()):
            if cow_id not in current_cow_ids:
                self.cows.remove(sprite)
                del self.cow_sprites[cow_id]
        # Add sprites for new cows
        for cow in self.env.cows:
            if cow.id not in self.cow_sprites:
                sprite = CowSprite(cow)
                self.cows.add(sprite)
                self.cow_sprites[cow.id] = sprite
        for sprite in self.cow_sprites.values():
            sprite.update()

    def draw_screen(self):
        """Draws the updated screen."""
        self.screen.blit(self.sky.image, self.sky.rect)
        self.screen.blit(self.back_sea.image, self.back_sea.rect)
        self.cliffs.draw(self.screen)
        self.cows.draw(self.screen)
        self.player.draw(self.screen)
        self.screen.blit(self.front_sea.image, self.front_sea.rect)

    def draw_text(self):
        """Draws score and lives text."""
        self.lives.update_text(self.env.lives)
        self.score.update_text(self.env.score)
        self.texts.draw(self.screen)

    def gameover_screen(self):
        """Renders game over screen."""
        self.draw_screen()

        self.game_over_texts = Group()
        self.game_over_texts.add(GameOverText(), FinalScoreSprite(self.env.score))
        self.game_over_texts.draw(self.screen)

        pygame.display.flip()
        # wait until a click to close
        wait = True
        while wait:
            for event in pygame.event.get():
                if (
                    event.type == pygame.QUIT
                    or event.type == pygame.MOUSEBUTTONDOWN
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)
                ):
                    wait = False

    @staticmethod
    def close():
        """Closes pygame."""
        pygame.quit()
