import pygame
from pygame.sprite import Group

from cowabunga.env.actions import Action
from cowabunga.env.settings import ACTION_COOLDOWN
from cowabunga.py_game.commands import CommandModes
from cowabunga.py_game.sprites.button import InfoButton, LeaderboardButton
from cowabunga.py_game.sprites.name_textbox import TextBoxSprite
from cowabunga.py_game.sprites.paddle import PaddleSprite
from cowabunga.py_game.sprites.text import PressToPlayText, TitleText
from cowabunga.py_game.states import States


class MainMenu:
    """Handles main menù for Cowabunga."""

    def __init__(self, commands: CommandModes, paddle: PaddleSprite, default_username: str):
        """Instantiates main menù elements.

        Args:
            commands: commands mode for paddle
            paddle: paddle sprite from pygame renderer.
            default_username: username that is initially displayed in the menù.
        """
        self.username = default_username
        self.paddle = paddle
        self.commands = commands
        self.main_menu_texts = Group()
        self.main_menu_texts.add(TitleText(), PressToPlayText())
        self.buttons = Group()
        self.buttons.add(LeaderboardButton(), InfoButton())
        self.ui = Group()
        self.ui.add(TextBoxSprite(text=self.username))

        self.frames_since_last_move = 0  # for paddle movement in menù

    def update(self):
        """Updates main menù."""
        # move paddle in menù
        action = self.paddle.get_key_input(self.commands)
        if action in (Action.LEFT, Action.RIGHT) and self.frames_since_last_move >= ACTION_COOLDOWN:
            self.paddle.paddle.move(action)
            self.frames_since_last_move = 0
        else:  # noqa: PLR5501
            if action != Action.NOOP_DRAG:
                self.paddle.paddle.animate_move()
        self.frames_since_last_move += 1
        self.ui.update()

    def draw(self, screen: pygame.Surface):
        """Draw the main menù. Must be called after PygameRenderer.draw_screen() to have background.

        Args:
            screen: surface to draw on.
        """
        self.main_menu_texts.draw(screen)
        self.buttons.draw(screen)
        self.ui.draw(screen)

    def handle_events(self) -> tuple[States, str]:
        """Handles main menù events.

        Returns:
            render_state: outcome of event handling.
            username: username entered in the textbox.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return States.CLOSE, self.username
            for element in self.ui.sprites():
                if isinstance(element, TextBoxSprite):
                    element.handle_event(event)
                    self.username = element.text
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons.sprites():
                    if isinstance(button, LeaderboardButton) and button.clicked(event.pos):
                        return States.LEADERBOARD, self.username
                    if isinstance(button, InfoButton) and button.clicked(event.pos):
                        return States.INFO, self.username
                for text in self.main_menu_texts.sprites():
                    if hasattr(text, "clicked") and text.clicked(event.pos):
                        return States.GAME, self.username
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return States.GAME, self.username
        return States.MENU, self.username
