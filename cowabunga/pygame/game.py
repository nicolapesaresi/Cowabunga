import pygame
import random
import sys
import json
from pygame.sprite import Group
import cowabunga.env.settings as settings
from pathlib import Path
from datetime import datetime
from cowabunga.env.env import CowabungaEnv
from cowabunga.env.objects.cow import Cow
from cowabunga.pygame.sprites.cow import CowSprite
from cowabunga.pygame.sprites.cliff import CliffSprite
from cowabunga.pygame.sprites.paddle import PaddleSprite
from cowabunga.pygame.sprites.sea import FrontSeaSprite, BackSeaSprite
from cowabunga.pygame.sprites.sky import SkySprite
from cowabunga.pygame.sprites.cloud import CloudSprite
from cowabunga.pygame.sprites.text import (
    LivesSprite,
    ScoreSprite,
)
from cowabunga.pygame.states import States
from cowabunga.pygame.main_menu import MainMenu
from cowabunga.pygame.gameover_screen import GameOver
from cowabunga.pygame.pause_screen import PauseScreen
from cowabunga.pygame.info_page import InfoPage
from cowabunga.pygame.leaderboard import LeaderboardScreen

# importing js only in browser mode
try:
    from js import window

    BROWSER_MODE = True
except ImportError:
    BROWSER_MODE = False


class PygameRenderer:
    """Pygame renderer for CowabungaEnv."""

    def __init__(
        self,
        screen: pygame.Surface | None = None,
        seed: int | None = None,
        start_at_menu: bool = True,
    ):
        """Initializes pygame renderer.
        Args:
            screen: None for desktop mode, pygame screen for browser.
            seed: seed to be passed to the env for random cow generation.
            menu: whether pygame starts form main menu or runs directly.
        """
        if screen is None:
            self.setup_pygame()
        else:
            self.screen = screen
        self.seed = seed
        self.fps = settings.FPS
        self.highscores_json = Path(__file__).parent / ".." / "highscores.json"
        self.username = settings.DEFAULT_USERNAME

        self.env = CowabungaEnv(self.seed)

        if start_at_menu:
            self.initial_state = States.MENU
        else:
            self.initial_state = States.GAME
        self.menu = None
        self.info = None
        self.gameover = None
        self.pause = None
        self.leaderboard = None
        # self.run()

    def setup_pygame(self):
        """Sets up pygame and screen for desktop mode."""
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Cowabunga - Pygame Edition")

    def main_menu(self):
        """Renders main menu of the game."""
        if not self.menu:
            self.menu = MainMenu(self.paddle, self.username)

        self.menu.update()
        self.draw_screen(move_background=True)
        self.menu.draw(self.screen)
        render_state, self.username = self.menu.handle_events()

        # if leaving menu, destroy menu to recreate next time
        if render_state != States.MENU:
            self.menu = None
        return render_state

    def leadernoard_page(self):
        """Renders leaderboard page."""
        if not self.leaderboard:
            scores = self.load_highscores()
            self.leaderboard = LeaderboardScreen(self.paddle, scores)
        self.leaderboard.update()
        self.draw_screen(move_background=True)
        self.leaderboard.draw(self.screen)
        render_state = self.leaderboard.handle_events()

        # if leaving leaderboard, destroy it to recreate next time
        if render_state != States.LEADERBOARD:
            self.leaderboard = None
        return render_state

    def info_page(self):
        """Renders info page."""
        if not self.info:
            self.info = InfoPage(self.paddle)

        self.info.update()
        self.draw_screen()
        self.info.draw(self.screen)
        render_state = self.info.handle_events()

        # if leaving info page, destroy it to recreate next time
        if render_state != States.INFO:
            self.info = None
        return render_state

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
        """Runs env loop in pygame desktop mode."""
        self.clock = pygame.time.Clock()
        self.load_gamescreen()

        render_state = self.initial_state

        running = True
        while running:
            if render_state == States.CLOSE:
                self.close()

            elif render_state == States.MENU:
                render_state = self.main_menu()

            elif render_state == States.INFO:
                render_state = self.info_page()

            elif render_state == States.LEADERBOARD:
                render_state = self.leadernoard_page()

            elif render_state == States.GAMEOVER:
                render_state = self.gameover_screen()

            elif render_state == States.PAUSE:
                render_state = self.pause_game()

            elif render_state == States.GAME:
                # main game logic
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        render_state = States.CLOSE
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        render_state = States.PAUSE

                # player input and env update
                self.paddle.get_key_input()
                self.env.step(
                    0
                )  # TODO: this only supports human player actions, change to support Agent
                self.update_cows()

                # draw new screen
                self.draw_screen()
                self.draw_text()

                # check game finished
                if self.env.done:
                    self.update_highscores(
                        name=self.username,
                        points=self.env.score,
                        timestamp=datetime.now(),
                    )
                    render_state = States.GAMEOVER
            pygame.display.flip()
            self.clock.tick(self.fps)
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
        to_remove = []
        for cloud in list(self.clouds):
            if (int(cloud.rect.x) > settings.WIDTH and cloud.speed >= 0) or (
                int(cloud.rect.x) + cloud.width < 0 and cloud.speed <= 0
            ):
                to_remove.append(cloud)
        self.clouds.update()
        for cloud in to_remove:
            cloud.kill()
        # spaw new clouds
        if (
            random.random() <= settings.NEW_CLOUD_PROB
            and len(self.clouds) < settings.MAX_CLOUDS_ON_SCREEN
        ):
            self.clouds.add(CloudSprite(x=settings.WIDTH))

    def draw_screen(self, move_background: bool = True):
        """Draws the updated screen.
        Args:
            move_background: if False, backgorund (sea and clouds) doesn't update.
        """
        if move_background:
            self.update_clouds()
            self.back_sea.update()
            self.front_sea.update()
        self.screen.blit(self.sky.image, self.sky.rect)
        self.clouds.draw(self.screen)
        self.back_sea.draw(self.screen)
        self.cliffs.draw(self.screen)
        self.cows.draw(self.screen)
        self.player.draw(self.screen)
        self.front_sea.draw(self.screen)

    def draw_text(self):
        """Draws score and lives text."""
        self.lives.update_text(self.env.lives)
        self.score.update_text(self.env.score)
        self.texts.draw(self.screen)

    def gameover_screen(self):
        """Renders game over screen."""
        if not self.gameover:
            self.gameover = GameOver(self.env.score)

        self.draw_screen(move_background=False)
        self.gameover.draw(self.screen)
        render_state = self.gameover.handle_events()

        # if leaving gameover screen, destroy it and reset env.
        if render_state != States.GAMEOVER:
            self.gameover = None
            self.env.reset()
            self.load_gamescreen()
        return render_state

    def pause_game(self):
        """Pauses the game until spacebar press."""
        if not self.pause:
            self.pause = PauseScreen()

        self.draw_screen(move_background=False)
        self.pause.draw(self.screen)
        self.draw_text()  # still draw lives and score
        render_state = self.pause.handle_events()

        # if leaving pause page, destroy it to recreate next time
        if render_state != States.PAUSE:
            self.pause = None
        return render_state

    @staticmethod
    def close():
        """Closes pygame."""
        pygame.quit()
        sys.exit()

    def load_highscores(self):
        """Loads highscores from json file or browser localStorage."""
        if BROWSER_MODE:
            data = window.localStorage.getItem("highscores")
            if data:
                return json.loads(data)
        with open(self.highscores_json, "r") as f:
            return json.load(f)

    def save_highscores(self, scores: dict):
        """Saves new highscores to json file or browser localStorage."""
        if BROWSER_MODE:
            window.localStorage.setItem("highscores", json.dumps(scores))
        else:
            with open(self.highscores_json, "w") as f:
                json.dump(scores, f, indent=2)

    def update_highscores(self, name: str, points: int, timestamp: datetime):
        highscores = self.load_highscores()
        highscores.append(
            {
                "name": name,
                "score": int(points),
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
            }
        )
        self.save_highscores(highscores)
