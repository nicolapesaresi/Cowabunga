import pygame

# import sys
# import pandas as pd
# from datetime import datetime
import cowabunga.env.settings as settings
from pathlib import Path
from cowabunga.env.env import CowabungaEnv
# from cowabunga.env.objects.cow import Cow
# from cowabunga.pygame.sprites.cow import CowSprite
# from cowabunga.pygame.sprites.cliff import CliffSprite
# from cowabunga.pygame.sprites.paddle import PaddleSprite
# from cowabunga.pygame.sprites.sea import FrontSeaSprite, BackSeaSprite
# from cowabunga.pygame.sprites.sky import SkySprite
# from cowabunga.pygame.sprites.cloud import CloudSprite
# from cowabunga.pygame.sprites.button import (
#     LeaderboardButton,
#     BackButton,
#     InfoButton,
#     PauseButton,
# )
# from cowabunga.pygame.sprites.leaderboard import LeaderboardScreen
# from cowabunga.pygame.sprites.info_page import InfoPage
# from cowabunga.pygame.sprites.name_textbox import TextBoxSprite
# from cowabunga.pygame.sprites.text import (
#     TitleText,
#     PressToPlayText,
#     LivesSprite,
#     ScoreSprite,
#     GameOverText,
#     FinalScoreSprite,
#     PressToGoToMenuText,
#     PauseText,
# )


class PygameRenderer:
    """Pygame renderer for CowabungaEnv."""

    def __init__(
        self,
        screen: pygame.Surface | None = None,
        seed: int | None = None,
        menu: bool = True,
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
        self.menu = menu
        self.seed = seed
        self.fps = settings.FPS
        self.highscores_csv = Path(__file__).parent / ".." / "highscores.csv"
        self.username = settings.DEFAULT_USERNAME

        self.env = CowabungaEnv(self.seed)
        # self.run()

    def setup_pygame(self):
        """Sets up pygame and screen for desktop mode."""
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Cowabunga - Pygame Edition")


#     def main_menu(self):
#         """Renders main menu of the game."""
#         main_menu_texts = Group()
#         main_menu_texts.add(TitleText(), PressToPlayText())
#         buttons = Group()
#         buttons.add(LeaderboardButton(), InfoButton())
#         ui = Group()
#         ui.add(TextBoxSprite(text=self.username))

#         # wait until a click to close
#         wait = True
#         while wait:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.close()
#                 for element in ui.sprites():
#                     if isinstance(element, TextBoxSprite):
#                         element.handle_event(event)
#                         self.username = element.text
#                 if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     for button in buttons.sprites():
#                         if isinstance(button, LeaderboardButton) and button.clicked(
#                             event.pos
#                         ):
#                             self.leaderboard_page()
#                         if isinstance(button, InfoButton) and button.clicked(event.pos):
#                             self.info_page()
#                 if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#                     wait = False

#             self.paddle.get_key_input()
#             self.draw_screen()
#             main_menu_texts.draw(self.screen)
#             buttons.draw(self.screen)
#             ui.update()
#             ui.draw(self.screen)
#             pygame.display.flip()

#             self.clock.tick(self.fps)

#     def leaderboard_page(self):
#         """Opens leaderboard page."""
#         df = pd.read_csv(self.highscores_csv)
#         df["score"] = df["score"].astype(int)
#         df = df.sort_values("score", ascending=False).reset_index()

#         leaderboard = LeaderboardScreen(df)
#         buttons = Group()
#         buttons.add(BackButton())

#         wait = True
#         while wait:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.close()
#                 elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     for button in buttons.sprites():
#                         if isinstance(button, BackButton) and button.clicked(event.pos):
#                             wait = False
#                 else:
#                     leaderboard.handle_event(event)

#             self.paddle.get_key_input()
#             self.draw_screen()
#             buttons.draw(self.screen)
#             leaderboard.draw(self.screen)
#             pygame.display.flip()
#             self.clock.tick(self.fps)

#     def info_page(self):
#         """Opens info page."""
#         buttons = Group()
#         buttons.add(BackButton())
#         info = InfoPage()

#         wait = True
#         while wait:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.close()
#                 elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                     for button in buttons.sprites():
#                         if isinstance(button, BackButton) and button.clicked(event.pos):
#                             wait = False

#             self.paddle.get_key_input()
#             self.draw_screen()
#             buttons.draw(self.screen)
#             info.draw(self.screen)
#             pygame.display.flip()
#             self.clock.tick(self.fps)

# def load_gamescreen(self):
#     """Loads main game elements, paddle and cliffs groups."""
#     self.paddle = PaddleSprite(self.env.paddle)
#     self.player = Group()
#     self.player.add(self.paddle)
#     self.cliffs = Group()
#     for cliff in self.env.cliffs:
#         self.cliffs.add(CliffSprite(cliff))
#     self.cow_sprites: dict[int, Cow] = {}
#     self.cows = Group()
#     self.update_cows()
#     # aestethics
#     self.sky = SkySprite()
#     self.back_sea = BackSeaSprite()
#     self.front_sea = FrontSeaSprite()
#     self.clouds = Group()
#     for i in range(2):
#         self.clouds.add(
#             CloudSprite(x=random.random() * settings.WIDTH / 2 + settings.WIDTH / 2)
#         )
#     # score and lives
#     self.lives = LivesSprite(self.env.lives)
#     self.score = ScoreSprite(self.env.score)
#     self.texts = Group()
#     self.texts.add(self.lives, self.score)

#     def run(self):
#         """Runs env loop in pygame."""
#         self.clock = pygame.time.Clock()
#         self.load_gamescreen()
#         running = True

#         self.main_menu()

#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                     self.pause_game()
#             # Player input
#             self.paddle.get_key_input()
#             self.env.step(
#                 0
#             )  # TODO: this only supports human player actions, change to support Agent
#             # Cow logic
#             self.update_cows()
#             # Drawing
#             self.draw_screen()
#             self.draw_text()
#             pygame.display.flip()

#             self.clock.tick(self.fps)
#             if self.env.done:
#                 self.update_highscores(
#                     name=self.username,
#                     points=self.env.score,
#                     timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#                 )
#                 self.gameover_screen()
#                 # when gameover screen is exited, reset env and go back to main menu
#                 self.env.reset()
#                 self.load_gamescreen()  # reloads sprites with new env
#                 self.main_menu()
#         self.close()

# def update_cows(self):
#     """Updates cow group using env info."""
#     current_cow_ids = {cow.id for cow in self.env.cows}
#     # Remove sprites for deleted cows
#     for cow_id, sprite in list(self.cow_sprites.items()):
#         if cow_id not in current_cow_ids:
#             self.cows.remove(sprite)
#             del self.cow_sprites[cow_id]
#     # Add sprites for new cows
#     for cow in self.env.cows:
#         if cow.id not in self.cow_sprites:
#             sprite = CowSprite(cow)
#             self.cows.add(sprite)
#             self.cow_sprites[cow.id] = sprite
#     for sprite in self.cow_sprites.values():
#         sprite.update()

#     def update_clouds(self):
#         """Updates and generates new clouds."""
#         for cloud in self.clouds:
#             if (cloud.rect.x > settings.WIDTH and cloud.speed > 0) or (
#                 cloud.rect.x < 0 - cloud.width and cloud.speed < 0
#             ):
#                 self.clouds.remove(cloud)
#                 cloud.kill()
#         self.clouds.update()
#         if (
#             random.random() <= settings.NEW_CLOUD_PROB
#             and len(self.clouds) < settings.MAX_CLOUDS_ON_SCREEN
#         ):
#             self.clouds.add(CloudSprite(x=settings.WIDTH))

#     def draw_screen(self):
#         """Draws the updated screen."""
#         self.screen.blit(self.sky.image, self.sky.rect)
#         self.update_clouds()
#         self.clouds.draw(self.screen)
#         self.back_sea.update()
#         self.back_sea.draw(self.screen)
#         self.cliffs.draw(self.screen)
#         self.cows.draw(self.screen)
#         self.player.draw(self.screen)
#         self.front_sea.update()
#         self.front_sea.draw(self.screen)

#     def draw_text(self):
#         """Draws score and lives text."""
#         self.lives.update_text(self.env.lives)
#         self.score.update_text(self.env.score)
#         self.texts.draw(self.screen)

#     def gameover_screen(self):
#         """Renders game over screen."""
#         self.draw_screen()
#         # buttons = Group()
#         # buttons.add(LeaderboardButton())
#         # buttons.draw(self.screen)
#         game_over_texts = Group()
#         game_over_texts.add(
#             GameOverText(), FinalScoreSprite(self.env.score), PressToGoToMenuText()
#         )
#         game_over_texts.draw(self.screen)

#         pygame.display.flip()
#         # wait until a click to close
#         wait = True
#         while wait:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.close()
#                 # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 #     for button in buttons.sprites():
#                 #         if isinstance(button, LeaderboardButton) and button.clicked(event.pos):
#                 #             self.leaderboard_page()
#                 #             wait = False
#                 elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#                     wait = False

#     @staticmethod
#     def close():
#         """Closes pygame."""
#         pygame.quit()
#         sys.exit()

#     def update_highscores(self, name: str, points: int, timestamp: datetime):
#         """Updates highscores csv with latest score.
#         Args:
#             name: name of the user.
#             points: points scored.
#             timestamp: timestamp of the game.
#         """
#         highscores = pd.read_csv(self.highscores_csv)
#         highscores.loc[len(highscores)] = [name, points, timestamp]
#         highscores.to_csv(self.highscores_csv, index=False)

#     def pause_game(self):
#         """Pauses the game until spacebar press."""
#         self.draw_screen()
#         buttons = Group()
#         buttons.add(PauseButton())
#         buttons.draw(self.screen)
#         pause_texts = Group()
#         pause_texts.add(PauseText())
#         pause_texts.draw(self.screen)

#         pygame.display.flip()
#         # wait until a click to continue with game
#         wait = True
#         while wait:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.close()
#                 elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#                     wait = False
