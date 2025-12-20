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
from cowabunga.pygame.sprites.cloud import CloudSprite
from cowabunga.pygame.sprites.text import (
    TitleText,
    PressToPlayText,
    LivesSprite,
    ScoreSprite,
    GameOverText,
    FinalScoreSprite,
    PressToGoToMenuText,
)


class PygameRenderer:
    """Pygame renderer for CowabungaEnv."""

    def __init__(self, seed: int | None = None, menu: bool = True):
        """Initializes pygame renderer.
        Args:
            seed: seed to be passed to the env for random cow generation.
            menu: whether pygame starts form main menu or runs directly.
        """
        self.menu = menu
        self.seed = seed
        self.fps = settings.FPS

        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Cowabunga - Pygame Edition")
        self.env = CowabungaEnv(self.seed)
        self.run()

    def main_menu(self):
        """Renders main menu of the game."""
        self.main_menu_texts = Group()
        self.main_menu_texts.add(TitleText(), PressToPlayText())

        # wait until a click to close
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                elif event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                ):
                    wait = False

            self.paddle.get_key_input()
            self.draw_screen()
            self.main_menu_texts.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(self.fps)

    def load_gamescreen(self):
        """Loads main game elements, paddle and cliffs groups."""
        self.paddle = PaddleSprite(self.env.paddle)
        self.player = Group()
        self.player.add(self.paddle)
        self.cliffs = Group()
        for cliff in self.env.cliffs:
            self.cliffs.add(CliffSprite(cliff))
        self.cow_sprites: dict[int, Cow] = {}
        self.cows = Group()
        self.update_cows()
        # aestethics
        self.sky = SkySprite()
        self.back_sea = BackSeaSprite()
        self.front_sea = FrontSeaSprite()
        self.clouds = Group()
        for i in range(2):
            self.clouds.add(
                CloudSprite(x=random.random() * settings.WIDTH / 2 + settings.WIDTH / 2)
            )
        # score and lives
        self.lives = LivesSprite(self.env.lives)
        self.score = ScoreSprite(self.env.score)
        self.texts = Group()
        self.texts.add(self.lives, self.score)

    def run(self):
        """Runs env loop in pygame."""
        self.clock = pygame.time.Clock()
        self.load_gamescreen()
        running = True

        self.main_menu()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Player input
            self.paddle.get_key_input()
            self.env.step(
                0
            )  # TODO: this only supports human player actions, change to support Agent
            # Cow logic
            self.update_cows()
            # Drawing
            self.draw_screen()
            self.draw_text()
            pygame.display.flip()

            self.clock.tick(self.fps)
            if self.env.done:
                self.gameover_screen()
                # when gameover screen is exited, reset env and go back to main menu
                self.env.reset()
                self.update_cows()  # removes leftover cow sprites before going back to menu
                self.main_menu()
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

    def update_clouds(self):
        """Updates and generates new clouds."""
        for cloud in self.clouds:
            if (cloud.rect.x > settings.WIDTH and cloud.speed > 0) or (
                cloud.rect.x < 0 - cloud.width and cloud.speed < 0
            ):
                self.clouds.remove(cloud)
                cloud.kill()
        self.clouds.update()
        if (
            random.random() <= settings.NEW_CLOUD_PROB
            and len(self.clouds) < settings.MAX_CLOUDS_ON_SCREEN
        ):
            self.clouds.add(CloudSprite(x=settings.WIDTH))

    def draw_screen(self):
        """Draws the updated screen."""
        self.screen.blit(self.sky.image, self.sky.rect)
        self.update_clouds()
        self.clouds.draw(self.screen)
        self.back_sea.update()
        self.back_sea.draw(self.screen)
        self.cliffs.draw(self.screen)
        self.cows.draw(self.screen)
        self.player.draw(self.screen)
        self.front_sea.update()
        self.front_sea.draw(self.screen)

    def draw_text(self):
        """Draws score and lives text."""
        self.lives.update_text(self.env.lives)
        self.score.update_text(self.env.score)
        self.texts.draw(self.screen)

    def gameover_screen(self):
        """Renders game over screen."""
        self.draw_screen()

        self.game_over_texts = Group()
        self.game_over_texts.add(
            GameOverText(), FinalScoreSprite(self.env.score), PressToGoToMenuText()
        )
        self.game_over_texts.draw(self.screen)

        pygame.display.flip()
        # wait until a click to close
        wait = True
        while wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                elif event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN
                ):
                    wait = False

    @staticmethod
    def close():
        """Closes pygame."""
        pygame.quit()
