import json
import random
import sys
from datetime import datetime
from pathlib import Path

import pygame
from pygame.sprite import Group

from cowabunga.env import settings
from cowabunga.env.env import CowabungaEnv
from cowabunga.env.objects.cow import Cow
from cowabunga.py_game.audio import AudioManager
from cowabunga.py_game.gameover_screen import GameOver
from cowabunga.py_game.info_page import InfoPage
from cowabunga.py_game.leaderboard import LeaderboardScreen
from cowabunga.py_game.main_menu import MainMenu
from cowabunga.py_game.pause_screen import PauseScreen
from cowabunga.py_game.settings_page import SettingsPage
from cowabunga.py_game.sprites.button import PauseButton
from cowabunga.py_game.sprites.cliff import CliffSprite
from cowabunga.py_game.sprites.cloud import CloudSprite
from cowabunga.py_game.sprites.cow import CowSprite
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.sprites.sea import BackSeaSprite, FrontSeaSprite
from cowabunga.py_game.sprites.sky import SkySprite
from cowabunga.py_game.sprites.text import (
    LivesSprite,
    ScoreSprite,
)
from cowabunga.py_game.states import States

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
            start_at_menu: whether pygame starts form main menu or runs directly.
        """
        if screen is None:
            self.setup_pygame()
        else:
            self.screen = screen
        self.seed = seed
        self.fps = settings.FPS
        self.highscores_json = Path(__file__).parent / ".." / "highscores.json"
        self.user_settings_json = Path(__file__).parent / ".." / "user_settings.json"
        self.username = settings.DEFAULT_USERNAME
        self.commands = settings.DEFAULT_COMMANDS

        self.env = CowabungaEnv(self.seed)
        self.audio = AudioManager()
        self.load_audio_settings()

        if start_at_menu:
            self.initial_state = States.MENU
        else:
            self.initial_state = States.GAME
        self.menu = None
        self.info = None
        self.gameover = None
        self.pause = None
        self.settings_page = None
        self.leaderboard = None
        # self.run()

    def setup_pygame(self):
        """Sets up pygame and screen for desktop mode."""
        pygame.mixer.pre_init(44100, -16, 2, 512)  # small buffer: low latency for bounce notes
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Cowabunga - Pygame Edition")

    def main_menu(self):
        """Renders main menu of the game."""
        if not self.menu:
            self.menu = MainMenu(self.commands, self.paddle, self.username)
        self.audio.start_music()
        self.audio.set_paused(False)
        self.audio.set_menu(True)

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
            self.leaderboard = LeaderboardScreen(self.commands, self.paddle, scores)
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
            self.info = InfoPage(self.commands, self.paddle)

        self.info.update()
        self.draw_screen()
        self.info.draw(self.screen)
        render_state, self.commands = self.info.handle_events()

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
        for _i in range(2):
            self.clouds.add(CloudSprite(x=random.random() * settings.WIDTH / 2 + settings.WIDTH / 2))
        # score and lives
        self.lives = LivesSprite(self.env.lives)
        self.score = ScoreSprite(self.env.score)
        self.texts = Group()
        self.texts.add(self.lives, self.score)
        # small pause button at the top center of the screen
        size = settings.WIDTH * 0.04
        self.pause_button = PauseButton(size, settings.WIDTH / 2 - size / 2, settings.HEIGHT * 0.03)

    def run(self):
        """Runs env loop in pygame desktop mode."""
        self.clock = pygame.time.Clock()
        self.load_gamescreen()

        render_state = self.initial_state

        while render_state != States.CLOSE:
            render_state = self.update_state(render_state)
            pygame.display.flip()
            self.clock.tick(self.fps)
        self.close()

    def update_state(self, render_state: States) -> States:
        """Renders one frame of the current state. Shared by desktop (run) and browser (main.py) loops.

        Args:
            render_state: current state.

        Returns:
            render_state: state for the next frame.
        """
        if render_state == States.MENU:
            render_state = self.main_menu()
        elif render_state == States.INFO:
            render_state = self.info_page()
        elif render_state == States.LEADERBOARD:
            render_state = self.leadernoard_page()
        elif render_state == States.GAMEOVER:
            render_state = self.gameover_screen()
        elif render_state == States.PAUSE:
            render_state = self.pause_game()
        elif render_state == States.SETTINGS:
            render_state = self.settings()
        elif render_state == States.GAME:
            render_state = self.game_step()
        self.audio.update()
        return render_state

    def game_step(self) -> States:
        """Runs one frame of the main game: input, env update, sounds and drawing."""
        render_state = States.GAME
        self.audio.start_music()  # in case the game starts without the menu
        self.audio.set_paused(False)
        self.audio.set_menu(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                render_state = States.CLOSE
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                render_state = States.PAUSE
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.pause_button.clicked(event.pos):
                render_state = States.PAUSE

        # player input and env update
        action = self.paddle.get_key_input(self.commands)
        _, done, info = self.env.step(action)  # TODO: this only supports human player actions, change to support Agent
        self.audio.process_events(info["events"])
        self.update_cows()

        # draw new screen
        self.draw_screen()
        self.draw_text()

        # check game finished
        if done:
            self.update_highscores(
                name=self.username,
                points=self.env.score,
                timestamp=datetime.now(),
            )
            render_state = States.GAMEOVER
        return render_state

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
        if random.random() <= settings.NEW_CLOUD_PROB and len(self.clouds) < settings.MAX_CLOUDS_ON_SCREEN:
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
        self.player.update()
        self.player.draw(self.screen)
        self.front_sea.draw(self.screen)

    def draw_text(self):
        """Draws score and lives text."""
        self.lives.update_text(self.env.lives)
        self.score.update_text(self.env.score)
        self.texts.draw(self.screen)
        self.screen.blit(self.pause_button.image, self.pause_button.rect)

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
        """Pause screen: volume settings, resume or quit to the main menu."""
        if not self.pause:
            self.pause = PauseScreen(self.audio)
        self.audio.set_paused(True)

        self.draw_screen(move_background=False)
        self.pause.draw(self.screen)
        self.draw_text()  # still draw lives and score
        render_state = self.pause.handle_events()

        # if leaving pause page, destroy it to recreate next time
        if render_state != States.PAUSE:
            self.pause = None
            self.save_audio_settings()
        if render_state == States.MENU:
            # the game is abandoned: no highscore, fresh game next time
            self.audio.sequencer.reset()
            self.env.reset()
            self.load_gamescreen()
        return render_state

    def settings(self):
        """Renders the sound settings page."""
        if not self.settings_page:
            self.settings_page = SettingsPage(self.audio)
        self.draw_screen()
        self.settings_page.draw(self.screen)
        render_state = self.settings_page.handle_events()

        # if leaving settings, destroy the page to recreate next time and remember the choice
        if render_state != States.SETTINGS:
            self.settings_page = None
            self.save_audio_settings()
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
        with open(self.highscores_json) as f:
            return json.load(f)

    def save_highscores(self, scores: dict):
        """Saves new highscores to json file or browser localStorage."""
        if BROWSER_MODE:
            window.localStorage.setItem("highscores", json.dumps(scores))
        else:
            with open(self.highscores_json, "w") as f:
                json.dump(scores, f, indent=2)

    def load_audio_settings(self):
        """Loads the player's volume settings from json file or browser localStorage."""
        try:
            if BROWSER_MODE:
                data = window.localStorage.getItem("audio_settings")
                values = json.loads(data) if data else {}
            elif self.user_settings_json.exists():
                with open(self.user_settings_json) as f:
                    values = json.load(f)
            else:
                values = {}
            self.audio.set_music_level(float(values.get("music", self.audio.music_level)))
            self.audio.set_sfx_level(float(values.get("sfx", self.audio.sfx_level)))
        except Exception as e:
            print(f"Unable to load audio settings, using defaults: {e}")

    def save_audio_settings(self):
        """Saves the player's volume settings to json file or browser localStorage."""
        values = {"music": round(self.audio.music_level, 2), "sfx": round(self.audio.sfx_level, 2)}
        try:
            if BROWSER_MODE:
                window.localStorage.setItem("audio_settings", json.dumps(values))
            else:
                with open(self.user_settings_json, "w") as f:
                    json.dump(values, f, indent=2)
        except Exception as e:
            print(f"Unable to save audio settings: {e}")

    def update_highscores(self, name: str, points: int, timestamp: datetime):
        """Updates highscores with new score."""
        highscores = self.load_highscores()
        highscores.append(
            {
                "name": name,
                "score": int(points),
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
            }
        )
        self.save_highscores(highscores)
