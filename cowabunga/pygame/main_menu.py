import pygame
from pygame.sprite import Group
from cowabunga.pygame.sprites.text import TitleText, PressToPlayText
from cowabunga.pygame.sprites.name_textbox import TextBoxSprite
from cowabunga.pygame.sprites.button import LeaderboardButton, InfoButton
from cowabunga.pygame.sprites.paddle import PaddleSprite
from cowabunga.pygame.states import States


class MainMenu:
    """Handles main menù for Cowabunga."""

    def __init__(self, paddle: PaddleSprite, default_username: str):
        """Instantiates main menù elements.
        Args:
            paddle: paddle sprite from pygame renderer.
            default_username: username that is initially displayed in the menù.
        """
        self.username = default_username
        self.paddle = paddle
        self.main_menu_texts = Group()
        self.main_menu_texts.add(TitleText(), PressToPlayText())
        self.buttons = Group()
        self.buttons.add(LeaderboardButton(), InfoButton())
        self.ui = Group()
        self.ui.add(TextBoxSprite(text=self.username))

    def update(self):
        """Updates main menù."""
        self.paddle.get_key_input()
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
                    if isinstance(button, LeaderboardButton) and button.clicked(
                        event.pos
                    ):
                        return States.LEADERBOARD, self.username
                    if isinstance(button, InfoButton) and button.clicked(event.pos):
                        return States.INFO, self.username
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return States.GAME, self.username
        return States.MENU, self.username
